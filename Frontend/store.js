import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
export default createStore({
  state: {
    connection: null,
    hosts: [],
    selectedHost: null,
    responses: [],
    graphData: [],

  },
  mutations: {
    setConnection(state, connection) {
      state.connection = connection;
    },
    setHosts(state, hosts) {
      state.hosts = hosts;
    },
    addHosts(state, hosts) {
      state.hosts = hosts;
    },
    setSelectedHost(state, host) {
      state.selectedHost = host;
    },
    updateHost(state, updatedHost) {
      const index = state.hosts.findIndex(
        (host) => host.identifier === updatedHost.identifier
      );
      if (index !== -1) {
        state.hosts.splice(index, 1, updatedHost);
      }
    },
    deleteHost(state, hostToDelete) {
      state.hosts = state.hosts.filter(
        (host) => host.identifier !== hostToDelete.identifier
      );
    },
    addResponse(state, responseData) {
      state.responses.push({ query: responseData.query, isClosed: false, ...responseData });
    },
    addGraphData(state, data) {
      state.graphData.push({
        query: data.query,
        ...data,
        isClosed: false,
      });
    },
    clearResponses(state) {
      state.responses = [];
    },
    clearGraphData(state) {
      state.graphData = [];
    },

    updateResponse(state, { index, data }) {
      if (state.responses[index]) {
        state.responses[index] = data;
      } 
    },
    
    updateGraphData(state, { index, data }) {
      state.graphData[index] = data;
    },
    filterResponses(state, uniqueResponses) {
      state.responses = state.responses.filter((response) =>
        uniqueResponses.includes(response.query.title)
      );
    },
    filterGraphData(state, uniqueResponses) {
      state.graphData = state.graphData.filter((response) =>
        uniqueResponses.includes(response.query.title)
      );
    },
  
    removeResponse(state, response) {
      const index = state.responses.findIndex(r => r.query === response.query);
      if (index >= 0) {
        state.responses.splice(index, 1);
      }
    },
    closeResponse(state, index) {
      if (index >= 0 && index < state.responses.length) {
        state.responses.splice(index, 1);
      } else {
        console.error(`Invalid index: ${index}`);
      }
    },
    reopenResponse(state, index) {
      state.responses[index].isClosed = false;
    },
    closeGraphData(state, queryTitle) {
      const index = state.graphData.findIndex(g => g.query === queryTitle);
      if (index >= 0) {
        state.graphData.splice(index, 1);
      }
    },

    reopenGraphData(state, index) {
      state.graphData[index].isClosed = false;
    } 
    
  },
  actions: {
    deleteHost({ commit }, hostToDelete) {
      commit("deleteHost", hostToDelete);
    },
  },
  plugins: [createPersistedState()],
});
