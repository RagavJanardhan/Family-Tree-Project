// familyTree.js

// Assuming you fetch the data from a Python server (AJAX or similar)
// If you're passing data directly, you'll load the structure manually as a test.

var nodes = new vis.DataSet([
    { id: 1, label: "Jay Janardhan", title: "Born: 1974-09-26", shape: 'box' },
    { id: 2, label: "Srilakshmi Kalyanasamy", title: "Born: 1976-07-16", shape: 'box' },
    { id: 3, label: "Ragav Janardhan", title: "Born: 2005-12-02", shape: 'circle' },
    { id: 4, label: "Janani Radhakrishnan", title: "Born: 2011-02-18", shape: 'circle' },
    { id: 5, label: "Sanjay Janardhan", title: "Born: 2003-08-05", shape: 'circle' },
    { id: 6, label: "Arjun Radhakrishnan", title: "Born: 2016-07-25", shape: 'circle' },
]);

var edges = new vis.DataSet([
    { from: 1, to: 3, label: "Father" },
    { from: 2, to: 3, label: "Mother" },
    { from: 1, to: 4, label: "Father" },
    { from: 2, to: 4, label: "Mother" },
    { from: 1, to: 5, label: "Father" },
    { from: 2, to: 5, label: "Mother" },
    { from: 3, to: 4, label: "Siblings" },
    { from: 3, to: 5, label: "Siblings" },
    { from: 4, to: 6, label: "Siblings" },
]);

var container = document.getElementById('familyTree');
var data = { nodes: nodes, edges: edges };
var options = {
    nodes: {
        font: { size: 14 },
        shape: 'box',
    },
    edges: {
        arrows: 'to',
    },
    layout: {
        hierarchical: {
            direction: 'UD',
        }
    }
};

var network = new vis.Network(container, data, options);
