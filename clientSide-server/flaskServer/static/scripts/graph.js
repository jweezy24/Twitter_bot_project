//scale that will be applied to weights
var scale = 1;
var nodes = [
    { group: 'nodes', data: { id: 'n0', label: 'n0', "visited": false }, classes: 'center-center' },
    { group: 'nodes', data: { id: 'n1', label: 'n1', "visited": false }, classes: 'center-center' },
    { group: 'nodes', data: { id: 'n3', label: 'n3', "visited": false }, classes: 'center-center' },
    { group: 'nodes', data: { id: 'n2', label: 'n2', "visited": false }, classes: 'center-center' },
    { group: 'nodes', data: { id: 'n4', label: 'n4', "visited": false }, classes: 'center-center', },
    { group: 'nodes', data: { id: 'n5', label: 'n5', "visited": false }, classes: 'center-center' },
    { group: 'nodes', data: { id: 'n6', label: 'n6', "visited": false }, classes: 'center-center' },
    { group: 'nodes', data: { id: 'n7', label: 'n7', "visited": false }, classes: 'center-center' },
    { group: 'nodes', data: { id: 'n8', label: 'n8', "visited": false }, classes: 'center-center', },
    { group: 'nodes', data: { id: 'n9', label: 'n9', "visited": false }, classes: 'center-center', }
]
var edges = [
    { group: 'edges', data: { id: 'e9', source: 'n7', target: 'n8', weight: 200, "visited": false } },
    { group: 'edges', data: { id: 'e0', source: 'n0', target: 'n1', weight: 100, "visited": false } },
    { group: 'edges', data: { id: 'e1', source: 'n1', target: 'n2', weight: 100, "visited": false } },
    { group: 'edges', data: { id: 'e2', source: 'n0', target: 'n2', weight: 150, "visited": false } },
    { group: 'edges', data: { id: 'e3', source: 'n0', target: 'n4', weight: 150, "visited": false } },
    { group: 'edges', data: { id: 'e4', source: 'n4', target: 'n2', weight: 200, "visited": false } },
    { group: 'edges', data: { id: 'e5', source: 'n4', target: 'n3', weight: 100, "visited": false } },
    { group: 'edges', data: { id: 'e6', source: 'n3', target: 'n5', weight: 100, "visited": false } },
    { group: 'edges', data: { id: 'e7', source: 'n3', target: 'n6', weight: 300, "visited": false } },
    { group: 'edges', data: { id: 'e8', source: 'n2', target: 'n7', weight: 100, "visited": false } },
    
    { group: 'edges', data: { id: 'e10', source: 'n4', target: 'n9', weight: 300, "visited": false } },
    { group: 'edges', data: { id: 'e11', source: 'n4', target: 'n8', weight: 200, "visited": false } }
]
//temporary also in future it will be array of nodes and array of edges
var elements = [...nodes.concat(edges)]

var cy;
$(document).ready(function () {
    cy = cytoscape({
        container: $("#cy"),
        autolock: false,

        elements: elements,
        layout: {
            name: 'cola',

        },
        style: [
            {
                "selector": "node[label]",
                "style": {
                    "label": "data(label)"
                }
            },
            {
                "selector": ".center-center",
                "style": {
                    "text-valign": "center",
                    "text-halign": "center"
                }
            },
        ]
    });
    var layout = cy.layout({ name: 'cola' }).run();
    layout.on('layoutstop', function () {
        //temporary location
        //setEdgeDistancesQueue();
        setEdgeDistances();
        elements.forEach(element => {
            if (element.group == 'nodes') {
                cy.$(`#${element.data.id}`).lock();
            }
        });

    })

})

function setEdgeDistances() {
    for (let i = 0; i < edges.length; i++) {

        var el1 = cy.$(`#${edges[i].data.source}`);
        var el2 = cy.$(`#${edges[i].data.target}`);

        if (el2.data('visited') == true) {

            continue;
        }
        //calculate distance and if it is not the same as weight*scale adjust it while keeping angle the same


        var dist = getDistance(el1.position(), el2.position())
        if (dist != edges[i].data.weight * scale) {
            //var difference = dist - elements[i].data.weight*scale;
            //console.log(difference);
            var angle = getAngle(el1.position(), el2.position());
            console.log(el1.id(), angle, el2.id())
            var x = edges[i].data.weight * scale * Math.cos(degrees_to_radians(angle - 90));
            //console.log(x);
            var y = edges[i].data.weight * scale * Math.sin(degrees_to_radians(angle - 90));
            el2.position({ x: x + el1.position('x'), y: y + el1.position('y') });
            console.log(el1.id(), getAngle(el1.position(), el2.position()), el2.id())
            console.log(el1.position(), el2.position());
            el1.data('visited', true);
            
        }

    }
}

var queue = [];

//main algorithm
function setEdgeDistancesQueue() {
    var start = cy.$(`#${elements[0].data.id}`)
    queue.push(start);

    while (queue.length > 0) {
        var node = queue.shift();
        node.data('visited', true);
        var connectedEdges = node.connectedEdges();
        connectedEdges.forEach((edge) => {
            //var source = cy.$(`#${edge.data('source')}`);
            var target = edge.target();
            console.log(node.id(), target.id());
            if (target.data('visited') == true || target.id() == node.id()) {
                return;
            }
            else {



                if (!queue.includes(target)) {
                    queue.push(target);
                }
                var dist = getDistance(node.position(), target.position())
                if (dist != edge.data('weight') * scale) {
                    //var difference = dist - elements[i].data.weight*scale;
                    //console.log(difference);
                    var angle = getAngle(node.position(), target.position());
                    console.log(node.id(), angle, target.id())
                    var x = edge.data('weight') * scale * Math.cos(degrees_to_radians(angle - 90));
                    console.log(x);
                    var y = edge.data('weight') * scale * Math.sin(degrees_to_radians(angle - 90));
                    target.position({ x: x + node.position('x'), y: y + node.position('y') });
                    //console.log(node.id(),getAngle(node.position(), target.position()),target.id())
                    console.log(node.position(), target.position());
                    target.data('visited', true);
                    
                }

            }

        })

    }
}

function degrees_to_radians(degree) {

    return degree * (Math.PI / 180);
}

//distance between two points
function getDistance(p1, p2) {
    return Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2));
}

function adjustLength(p1, p2) {

}

//angle between two points
function getAngle(p1, p2) {
    // var angle = (Math.atan2(p2.y-p1.y, p2.x-p1.x) * 180) / Math.PI;
    // if (angle < 0) { angle += 360 }
    var p3 = { x: p1.x, y: p1.y - 10 }

    var p12 = getDistance(p2, p1);
    var p13 = getDistance(p3, p1);
    var p23 = getDistance(p3, p2);

    var angle = Math.acos(((Math.pow(p12, 2)) + (Math.pow(p13, 2)) - (Math.pow(p23, 2))) / (2 * p12 * p13)) * 180 / Math.PI;
    if (p2.x < p1.x) {
        angle = 360 - angle;
    }
    return angle;
}




