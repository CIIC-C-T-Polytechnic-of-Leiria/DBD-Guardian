<template>
  <div class="grid-container">
    <div v-for="host in hosts" :key="host.identifier" class="grid-item">
      <h3 class="host-title">{{ host.identifier }}</h3>
      <hr class="delimiter" />
      <fieldset class="nice-form-group">
        <legend>Datasources</legend>
        <div
          v-for="datasource in host.datasourcesArray"
          :key="datasource.name"
          class="nice-form-group"
        >
          <input
            type="checkbox"
            :id="datasource.name"
            :value="datasource.name"
            @change="
              toggleDatasourceSelection(datasource.name, host.identifier)
            "
          />
          <label :for="datasource.name">{{ datasource.name }}</label>
        </div>
      </fieldset>
    </div>
  </div>
  <div class="query-container" v-if="selectedDatasources.length">
    <div
      class="nice-form-group"
      @mouseover="showTooltip = true"
      @mouseout="showTooltip = false"
    >
      <label>Queries</label>
      <select v-model="selectedQuery" :key="filteredQueryTitles.length">
        <option
          v-for="query in filteredQueryTitles"
          :key="query.title"
          :value="query"
        >
          {{ query.title }}
        </option>
      </select>
      <div class="tooltip" v-if="showTooltip">
        {{ selectedQuery?.description }}
      </div>
    </div>
    <NormalButton @click="executeQuery" class="normalbtn">
      Add to Dashboard
    </NormalButton>
  </div>
  <div class="list-grid">
    <div
      class="custom-flex-column"
      v-for="(item, index) in responses"
      :key="'list-' + index"
    >
      <ListComponent :data="item" :index="index" @close="closeQuery" />
    </div>
  </div>
  <div class="graph-grid">
    <div class="custom-flex-column">
      <GraphComponent
        v-for="graph in graphData"
        :key="graph.query"
        :data="graph"
        @closeGraph="closeGraph"
      />
    </div>
  </div>
</template>
<script>
import { mapMutations } from "vuex";
import axios from "axios";
import NormalButton from "./NormalButton.vue";
import ListComponent from "./ListComponent.vue";
import GraphComponent from "./GraphComponent.vue";
export default {
  name: "AnalyticsPage",
  components: {
    NormalButton,
    ListComponent,
    GraphComponent,
  },
  data() {
    return {
      selectedHosts: [],
      selectedDatasources: [],
      selectedQuery: null,
      hosts: [],
      queryTitles: [],
      type: "1",
      selectedParses: [],
      dashboardItems: [],
      showTooltip: false,
    };
  },
  created() {
    this.getHosts(); // Initial call
    this.hostsInterval = setInterval(() => {
      this.getHosts();
    }, 30000);

    axios
      .get("http://localhost:5000/getqueries")
      .then((response) => {
        this.queryTitles = response.data;
        console.log(this.queryTitles);
      })
      .catch((error) => {
        console.error(error);
      });
    this.startPolling();
  },
  methods: {
    getHosts() {
      axios
        .get("http://localhost:5000/gethosts")
        .then((response) => {
          this.hosts = Object.entries(response.data).map(
            ([identifier, hostData]) => ({
              identifier,
              datasourcesArray: Object.entries(hostData.datasources).map(
                ([name, parse]) => ({
                  name,
                  parse,
                })
              ),
            })
          );
        })
        .catch((error) => {
          console.error(error);
        });
    },
    closeQuery(index) {
      this.$store.commit("closeResponse", index);
    },
    closeGraph(queryTitle) {
      this.$store.commit("closeGraphData", queryTitle);
    },
    ...mapMutations(["addResponse", "addGraphData"]),

    toggleDatasourceSelection(datasourceName, hostIdentifier) {
      const index = this.selectedDatasources.findIndex(
        (ds) => ds.name === datasourceName && ds.host === hostIdentifier
      );

      // Check if the host and datasource still exist
      const selectedHost = this.hosts.find(
        (host) => host.identifier === hostIdentifier
      );
      const datasourceExists =
        selectedHost &&
        selectedHost.datasourcesArray.some((ds) => ds.name === datasourceName);

      if (index >= 0) {
        this.selectedDatasources.splice(index, 1);
      } else if (datasourceExists) {
        // If the datasource still exists, add it to the selectedDatasources list
        const selectedDatasource = selectedHost.datasourcesArray.find(
          (ds) => ds.name === datasourceName
        );
        this.selectedDatasources.push({
          name: datasourceName,
          host: hostIdentifier,
          parse: selectedDatasource.parse,
        });
      }

      // Clean up the selectedDatasources list to remove any datasources that no longer exist
      for (let i = this.selectedDatasources.length - 1; i >= 0; i--) {
        const ds = this.selectedDatasources[i];
        const hostExists = this.hosts.some(
          (host) => host.identifier === ds.host
        );
        const datasourceStillExists =
          hostExists &&
          this.hosts
            .find((host) => host.identifier === ds.host)
            .datasourcesArray.some((source) => source.name === ds.name);

        if (!hostExists || !datasourceStillExists) {
          this.selectedDatasources.splice(i, 1);
        }
      }

      this.updateTypeAndParses();
    },

    updateTypeAndParses() {
      let hostsWithSelectedDatasources = [];
      this.selectedDatasources.forEach((selectedDs) => {
        this.hosts.forEach((host) => {
          if (host.identifier === selectedDs.host) {
            const ds = host.datasourcesArray.find(
              (ds) => ds.name === selectedDs.name
            );
            if (ds && !hostsWithSelectedDatasources.includes(host)) {
              hostsWithSelectedDatasources.push(host);
            }
          }
        });
      });
      const selectedHostCount = hostsWithSelectedDatasources.length;
      if (selectedHostCount > 1) {
        this.type = "3";
      } else if (this.selectedDatasources.length > 1) {
        this.type = "2";
      } else {
        this.type = "1";
      }

      this.selectedParses = this.selectedDatasources.map((ds) => ds.name);
    },
    startPolling() {
      setInterval(() => {
        // Execute the query
        this.executeQueryPolling();
      }, 30000);
    },

    executeQueryCommon(queryTitle, queryType) {
      const hostIdentifiers = [
        ...new Set(this.selectedDatasources.map((ds) => ds.host)),
      ];
      const dataSources = this.selectedDatasources.map((ds) => {
        return {
          identifier: ds.host,
          dataSources: [ds.name],
        };
      });

      // Create an axios instance
      const instance = axios.create({
        baseURL: "http://localhost:5000",
        headers: {
          "Content-Type": "application/json",
        },
      });

      // Send the POST request
      return instance.post("/execquery", {
        hostIdentifiers,
        dataSources,
        queryTitle,
        queryType,
      });
    },

    executeQuery() {
      const queryTitle = this.selectedQuery.title;
      const queryType = this.selectedQuery.type;

      // Find existing response or graph data for the selected query
      const existingResponseIndex = this.responses.findIndex(
        (r) => r.query === queryTitle
      );
      const existingGraphDataIndex = this.graphData.findIndex(
        (g) => g.query === queryTitle
      );

      // Reopen if closed
      if (
        existingResponseIndex >= 0 &&
        this.responses[existingResponseIndex].isClosed
      ) {
        this.$store.commit("reopenResponse", existingResponseIndex);
      }
      if (
        existingGraphDataIndex >= 0 &&
        this.graphData[existingGraphDataIndex].isClosed
      ) {
        this.$store.commit("reopenGraphData", existingGraphDataIndex);
      }

      this.executeQueryCommon(queryTitle, queryType)
        .then((response) => {
          const responseData = Object.values(response.data)[0];
          if (
            responseData.return_type === "1" &&
            !this.responses.some((r) => r.query === responseData.query)
          ) {
            this.addResponse(responseData);
          } else if (
            responseData.return_type === "2" &&
            !this.graphData.some((g) => g.query === responseData.query)
          ) {
            this.addGraphData(responseData);
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },

    executeQueryPolling() {
      // Filter out the queries that are closed
      const activeQueries = this.responses.filter(
        (response) => !response.isClosed
      );
      const activeGraphs = this.graphData.filter((graph) => !graph.isClosed);

      // Combine active responses and graphData
      const combinedData = [...activeQueries, ...activeGraphs];
      // Combine active responses and graphData for promise execution
      const promises = combinedData.map((response) => {
        // Execute the common query execution code and return the promise
        return this.executeQueryWithDatasource(response.query_data);
      });

      Promise.all(promises)
        .then((responses) => {
          responses.forEach((response, index) => {
            const responseData = Object.values(response.data)[0];
            if (!responseData) {
              // Determine whether to close a response or a graph based on the return type
              if (combinedData[index].return_type === "1") {
                // Close the response
                this.closeQuery(index);
              } else if (combinedData[index].return_type === "2") {
                // Close the graph

                const queryTitleForGraph =
                  combinedData[index].query_data.queryTitle;

                this.closeGraph(queryTitleForGraph);
              }
              return;
            }
            if (responseData.return_type === "1") {
              const existingResponseIndex = this.responses.findIndex(
                (r) => r.query === responseData.query
              );

              if (
                existingResponseIndex >= 0 &&
                !this.responses[existingResponseIndex].isClosed
              ) {
                // Merge the new data with the existing response
                Object.assign(
                  this.responses[existingResponseIndex],
                  responseData
                );

                this.$store.commit("updateResponse", {
                  index: existingResponseIndex,
                  data: this.responses[existingResponseIndex],
                });
              }
            } else if (responseData.return_type === "2") {
              const existingGraphDataIndex = this.graphData.findIndex(
                (g) => g.query === responseData.query
              );

              if (
                existingGraphDataIndex >= 0 &&
                !this.graphData[existingGraphDataIndex].isClosed
              ) {
                // Merge the new data with the existing graph data
                Object.assign(
                  this.graphData[existingGraphDataIndex],
                  responseData
                );

                this.$store.commit("updateGraphData", {
                  index: existingGraphDataIndex,
                  data: this.graphData[existingGraphDataIndex],
                });
              }
            }
          });
        })
        .catch((error) => {
          console.error(error);
        });
    },

    executeQueryWithDatasource(queryData) {
      // Create an axios instance
      const instance = axios.create({
        baseURL: "http://localhost:5000",
        headers: {
          "Content-Type": "application/json",
        },
      });

      // Send the POST request
      return instance.post("/execquery", queryData);
    },
  },
  computed: {
    responses() {
      return this.$store.state.responses;
    },
    graphData() {
      return this.$store.state.graphData;
    },
    filteredQueryTitles() {
      const filtered = this.queryTitles.filter((query) => {
        if (query.type !== this.type) {
          return false;
        }
        
        const selectedParses = this.selectedDatasources.map((ds) => ds.parse);

        if (this.type !== "3" && query.parse.length !== selectedParses.length) {
          return false;
        }

        const sortedQueryParse = [...query.parse].sort();
        const sortedSelectedParses = [...selectedParses].sort();

        // If type is 3, we only need to check that each parse type in the query is present in the selected datasources
        // and each parse type in the selected datasources is present in the query parse types
        if (this.type === "3") {
          for (let i = 0; i < sortedQueryParse.length; i++) {
            if (!sortedSelectedParses.includes(sortedQueryParse[i])) {
              return false;
            }
          }
          for (let i = 0; i < sortedSelectedParses.length; i++) {
            if (!sortedQueryParse.includes(sortedSelectedParses[i])) {
              return false;
            }
          }
        } else {
          // Else, we continue checking as before
          for (let i = 0; i < sortedQueryParse.length; i++) {
            if (sortedQueryParse[i] !== sortedSelectedParses[i]) {
              return false;
            }
          }
        }
        return true;
      });
      
      return filtered;
    },
    listItems() {
      // Convert this.responses from an object to an array
      return Object.values(this.responses);
    },
  },

  watch: {
    filteredQueryTitles(newVal) {
      if (!this.selectedQuery && newVal.length > 0) {
        this.selectedQuery = newVal[0];
      }
    },
  },
  beforeUnmount() {
    clearInterval(this.hostsInterval);
  },
};
</script>

<style scoped>
.nice-form-group {
    position: relative;
}
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;
}

.grid-item {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
}

.host-title {
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 10px;
}

.delimiter {
  border: 0;
  border-top: 2px solid #0084ff;
  margin-bottom: 10px;
}

.query-container {
  max-width: 600px;
  margin: 20px auto 0;
  padding: 20px;
}
.normalbtn {
    display: block;
    margin-top: 40px;  /* Increase this from the original 20px */
    margin-bottom: 50px;
    margin-left: auto;
    margin-right: auto;
}
.custom-flex-column {
  display: flex;
  flex-direction: column;
  align-items: normal;
}
.list-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  grid-gap: 1em;
  grid-auto-rows: minmax(100px, auto); /* New line added */
  padding: 1em;
}
.graph-container {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  margin-top: 2em; /* Add some space between lists and graphs */
}
.graph-grid {
  display: flex;
  flex-direction: column;
}
.tooltip {
  position: absolute;
  background-color: #333;
  color: white;
  padding: 8px 10px;
  border-radius: 4px;
  font-size: 12px;
  top: calc(100% + 5px); /* position below the select */
  left: 50%; /* centering the tooltip */
  transform: translateX(-50%); /* centering the tooltip */
  white-space: nowrap; /* prevent text wrapping */
  opacity: 0.9;
  z-index: 10;
}
</style>
