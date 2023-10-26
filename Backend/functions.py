from flask import request, current_app as app
from werkzeug.utils import secure_filename


import os
import glob
import json
from datetime import datetime

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'json'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(folder):
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
                # Delete all files in the directory
        files = glob.glob(folder + '/*')
        for f in files:
            os.remove(f)
        filename = secure_filename(file.filename)
        file.save(os.path.join(folder, filename))
        return 'File uploaded successfully', 200
    else:
        return 'Unsupported file type', 400

def query_build(title, dsPaths, privacy):
    # Load the queries and parsers from the JSON files
    if not privacy:
        with open(app.config['queries'], 'r') as f:
            queries = json.load(f)
    else:
        with open(app.config['queries_priv'], 'r') as f:
            queries = json.load(f)

    with open(app.config['parse'], 'r') as f:
        parsers = json.load(f)

    # Find the query for the given title
    title = title.strip().lower()  # Remove spaces and convert to lower case
    query_info = next((q for q in queries if q['title'].strip().lower() == title), None)
  #  print(f"Query info: {query_info}")
    # If there's no query_info with the provided title, return None or handle this case appropriately
    if query_info is None:
       # print(f"Query with title '{title}' not found in queries file.")
        return None, None

    # Create a mapping for the format function
    format_mapping = {}

    # Iterate over the parsers in query_info
    for i, parser in enumerate(query_info['parse']):
        # Find the corresponding path and parser for this parser
        path_parser = next((pp for pp in dsPaths if pp[1] == parser), None)
       # print(f"Path parser: {path_parser}")
        if path_parser is None:
            #print(f"Path and parser for parser '{parser}' not found in dsPaths.")
            continue
        file, parsing_type = path_parser
        parser_info = next((p for p in parsers if p['parse'] == parsing_type), None)
        #print(f"Parser info: {parser_info}")
        if parser_info is None:
            #print(f"Parser info for parsing type '{parsing_type}' not found in parsers file.")
            continue
        #print(f"query_info['query']: {query_info['query']}")
        if i == 0:  # The first parser and file don't have a number suffix in the placeholder
            #print(f"Parser_info['query']: {parser_info['query']}")
            format_mapping['parser'] = parser_info['query']
            #print(f"File: {file}")
            format_mapping['file'] = file
        else:  # The subsequent parsers and files have a number suffix in the placeholder
            #print(f"Parser_info['query']: {parser_info['query']}")
            format_mapping[f'parser{i}'] = parser_info['query']
            #print(f"File: {file}")
            format_mapping[f'file{i}'] = file

    # Format the query with the format_mapping
    try:
        #print(f"Format mapping: {format_mapping}")
        final_query = query_info['query'].format(**format_mapping)
    except KeyError as e:
        #print(f"KeyError while formatting query: {e}")
        return None, None

    # Get the return type from the query_info
    return_type = query_info.get('return', None)  # None is the default value if 'return' key is not found

    return final_query, return_type

def aggregate_results(results):
    aggregated_results = []
    for result in results:
        aggregated_results.extend(result["result"])
    return aggregated_results

def process_results(final_results, query_title):
    
    if query_title == 'Users With Failed Login Attempts in the Last Day Across the Network':
        user_occurrences = {}
        user_counts = {}
        
        for host_result in final_results:
            if host_result['result'] == "No results found" or not isinstance(host_result['result'], list):
                continue
            seen_users_in_host = set()
            for item in host_result['result']:
                line = item[0]
                user_start = line.find('#User:# ') + len('#User:# ')
                user_end = line.find(' ', user_start)
                user = line[user_start:user_end]
                count_start = line.rfind('# ') + len('# ')
                count = int(line[count_start:])
                seen_users_in_host.add(user)
                
                # Increment or set the user count
                user_counts[user] = user_counts.get(user, 0) + count

            for user in seen_users_in_host:
                # Increment or set the user occurrences
                user_occurrences[user] = user_occurrences.get(user, 0) + 1
        total_hosts = len(final_results)
        users_in_all_hosts = {user for user, occurrences in user_occurrences.items() if occurrences == total_hosts}
        output = [['#User:# ' + user + ' #Total Failed Attempts:# ' + str(user_counts[user])] for user in users_in_all_hosts]
        if output:
            return {"output": output, "graphType": ""}
        else:
            return {"output": "No results found", "graphType": ""}
        
    elif query_title == 'IP Addresses With The Most Requests in the Last Hour':
        ip_counts = {}
        for host_result in final_results:
            if host_result['result'] == "No results found" or not isinstance(host_result['result'], list):
                continue  # Skip this host if the result is not a list
            for item in host_result['result']:
                ip = item[0].split(' ')[1]
                count = int(item[0].split(' ')[-1])  # corrected index for count
                if ip in ip_counts:
                    ip_counts[ip] += count
                else:
                    ip_counts[ip] = count
        high_request_ips = {ip: count for ip, count in ip_counts.items() if count > 0}
        output = [['#Address:# ' + ip + ' #Total Requests:# ' + str(count)] for ip, count in high_request_ips.items()]
        if output:
            return {"output": output, "graphType": ""}
        else:
            return {"output": "No results found", "graphType": ""}
 
    elif query_title == 'Failed Login Attempts Per Hour':
        hour_counts = {}
        for host_result in final_results:
           
            
            if host_result['result'] == "No results found" or not isinstance(host_result['result'], list):
                continue
            for item in host_result['result']:
                # Extract full date and time
                hour_raw = ' '.join(item[0].split(' ')[1:4])
                hour = hour_raw.split(".")[0]
                count = int(item[0].split(' ')[7])  # extract count
                if hour in hour_counts:
                    hour_counts[hour] += count
                else:
                    hour_counts[hour] = count
        output = []
        for hour, count in hour_counts.items():
            output.append(['#Hour:# ' + hour + ' #Total Failed Attempts:# ' + str(count)])
        if output:
            return {"output": output, "graphType": "line"}
        else:
            return {"output":['#Hour:# ' + "No results found" + ' #Total Failed Attempts:# ' + "No results found"], "graphType": "line"}
    elif query_title == 'Incoming Packets Per Hour':
        hour_counts = {}
        for host_result in final_results:
            if host_result['result'] == "No results found" or not isinstance(host_result['result'], list):
                continue
            for item in host_result['result']:
                # Extract full date and time
                hour_raw = ' '.join(item[0].split(' ')[1:4])
                hour = hour_raw.split(".")[0]
                count = int(item[0].split(' ')[7])  # extract count
                if hour in hour_counts:
                    hour_counts[hour] += count
                else:
                    hour_counts[hour] = count
        output = []
        for hour, count in hour_counts.items():
            output.append(['#Hour:# ' + hour + ' #Total Incoming Packets:# ' + str(count)])
        if output:
            return {"output": output, "graphType": "line"}
        else:
            return {"output":['#Hour:# ' + "No results found" + ' #Total Incoming Packets:# ' + "No results found"], "graphType": "line"}
    elif query_title == 'Number of Warning/Error Messages in Syslog per Hour':  
        hour_counts = {}
       # print(final_results)
        
        for host_result in final_results:
            if host_result['result'] == "No results found" or not isinstance(host_result['result'], list):
                continue
            for item in host_result['result']:
                # Extract full date and time
                hour_raw = ' '.join(item[0].split(' ')[1:4])
                hour = hour_raw.split(".")[0]

                # Extract count
                count_str = item[0].split(' ')[7]
                count = int(count_str)

                if hour in hour_counts:
                    hour_counts[hour] += count
                else:
                    hour_counts[hour] = count

        output = []
        for hour, count in hour_counts.items():
            output.append(['#Hour:# ' + hour + ' #Total Warnings/Errors:# ' + str(count)])
        if output:
            print(output)
            return {"output": output, "graphType": "bar"}
        else:
             return {"output":['#Hour:# ' + "No results found" + ' #Total Warnings/Errors:# ' + "No results found"], "graphType": "line"}
    elif query_title == 'Number of requests made to the database per Hour':
        hour_counts = {}

        for item in final_results:
            # Each item is a list with a single string, so we get the string
            item_str = item[0]

            # Extract hour and remove ".000 Europe/London"
            hour_raw = item_str.split(' ')[1:4]
            hour = ' '.join(hour_raw).replace('.000 Europe/London', '')
            print(hour)
            # Extract count
            count_str = item_str.split(' ')[-1]
            count = int(count_str)

            # Aggregate count for each hour
            if hour in hour_counts:
                hour_counts[hour] += count
            else:
                hour_counts[hour] = count

        # Convert aggregated counts to the desired output format
        output = []
        for hour, count in hour_counts.items():
            output.append(['#Hour:# ' + hour + ' #Total Requests:# ' + str(count)])

        # Return results based on whether we have any output
        if output:
            print(output)
            return {"output": output, "graphType": "bar"}
        else:
            return {"output": ['No results found'], "graphType": "line"}

    else:
        return "No results found"

