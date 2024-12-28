// familyTree.js

// Data for the family tree nodes
var nodes = new vis.DataSet([
    { id: 1, label: "Jay Janardhan", title: "Born: 1974-09-26", shape: 'box', color: '#FFB6C1' },
    { id: 2, label: "Srilakshmi Kalyanasamy", title: "Born: 1976-07-16", shape: 'box', color: '#FFB6C1' },
    { id: 3, label: "Ragav Janardhan", title: "Born: 2005-12-02", shape: 'ellipse', color: '#90EE90' },
    { id: 4, label: "Sanjay Janardhan", title: "Born: 2003-08-05", shape: 'ellipse', color: '#90EE90' },
]);

// Data for the family tree edges (relationships)
var edges = new vis.DataSet([
    { from: 1, to: 3, label: "Father", color: '#000000' },
    { from: 2, to: 3, label: "Mother", color: '#000000' },
    { from: 1, to: 4, label: "Father", color: '#000000' },
    { from: 2, to: 4, label: "Mother", color: '#000000' },
    { from: 3, to: 4, label: "Siblings", color: '#000000' },
]);

// Container for the family tree visualization
var container = document.getElementById('familyTree');

// Create the data object for Vis.js
var data = {
    nodes: nodes,
    edges: edges
};

// Options for the network visualization
var options = {
    nodes: {
        font: { size: 16, face: 'Arial' }, // Increase font size
        shape: 'ellipse',  // Ensure consistent shape for all nodes
        size: 30, // Set a consistent node size
        color: {
            background: '#90EE90',
            border: '#006400',
        }
    },
    edges: {
        arrows: { to: { enabled: true, scaleFactor: 0.5 } }, // Add arrowheads to edges
        color: '#000000',
        font: { size: 12 },
        smooth: { type: 'continuous' }, // Smooth out edges
    },
    layout: {
        hierarchical: {
            direction: 'UD', // 'UD' means Top to Bottom (Upwards)
            sortMethod: 'directed', // Maintain directed structure
            levelSeparation: 100, // Increase separation between levels
            nodeSpacing: 150, // Increase space between nodes
            shakeTowards: 'roots', // Ensure siblings stay at the same level
            blockThreshold: 1, // Ensures only children at the same level are moved horizontally
        }
    },
    physics: {
        enabled: false,  // Disable physics for a more static layout
    }
};

// Initialize the network
var network = new vis.Network(container, data, options);
