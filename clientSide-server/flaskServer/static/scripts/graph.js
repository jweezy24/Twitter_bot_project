//scale that will be applied to weights
var scale = 500;
// var oldNodes = [
//     { group: 'nodes', data: { id: 'n0', label: 'n0', visited: false, followers:100, following:1000 ,image:'https://live.staticflickr.com/1261/1413379559_412a540d29_b.jpg' }, classes: 'center-center', },
//     { group: 'nodes', data: { id: 'n1', label: 'n1', "visited": false }, classes: 'center-center' },
//     { group: 'nodes', data: { id: 'n3', label: 'n3', "visited": false }, classes: 'center-center' },
//     { group: 'nodes', data: { id: 'n2', label: 'n2', "visited": false }, classes: 'center-center' },
//     { group: 'nodes', data: { id: 'n4', label: 'n4', "visited": false }, classes: 'center-center', },
//     { group: 'nodes', data: { id: 'n5', label: 'n5', "visited": false }, classes: 'center-center' },
//     { group: 'nodes', data: { id: 'n6', label: 'n6', "visited": false }, classes: 'center-center' },
//     { group: 'nodes', data: { id: 'n7', label: 'n7', "visited": false }, classes: 'center-center' },
//     { group: 'nodes', data: { id: 'n8', label: 'n8', "visited": false }, classes: 'center-center', },
//     { group: 'nodes', data: { id: 'n9', label: 'n9', "visited": false }, classes: 'center-center', }
// ]
// var oldEdges = [

//     { group: 'edges', data: { id: 'e0', source: 'n0', target: 'n1', weight: 100, "visited": false } },
//     // { group: 'edges', data: { id: 'e1', source: 'n1', target: 'n2', weight: 100, "visited": false } },
//     //{ group: 'edges', data: { id: 'e2', source: 'n0', target: 'n2', weight: 150, "visited": false } },
//     { group: 'edges', data: { id: 'e3', source: 'n0', target: 'n4', weight: 150, "visited": false } },
//     { group: 'edges', data: { id: 'e4', source: 'n4', target: 'n2', weight: 200, "visited": false } },
//     { group: 'edges', data: { id: 'e5', source: 'n4', target: 'n3', weight: 100, "visited": false } },
//     { group: 'edges', data: { id: 'e6', source: 'n3', target: 'n5', weight: 100, "visited": false } },
//     { group: 'edges', data: { id: 'e7', source: 'n3', target: 'n6', weight: 300, "visited": false } },
//     { group: 'edges', data: { id: 'e8', source: 'n2', target: 'n7', weight: 200, "visited": false } },
//     { group: 'edges', data: { id: 'e9', source: 'n7', target: 'n8', weight: 200, "visited": false } },
//     { group: 'edges', data: { id: 'e10', source: 'n4', target: 'n9', weight: 300, "visited": false } },
//     //{ group: 'edges', data: { id: 'e11', source: 'n4', target: 'n8', weight: 200, "visited": false } }
// ]
//temporary also in future it will be array of nodes and array of edges
var elements = [...nodes.concat(edges)]
var addedElements = []
var addedNodes = []
var addedEdges = []

var cy;
var previousTapStamp;
var doubleClickDelayMs = 350;

$(document).ready(function () {
    console.log(elements)

    cy = cytoscape({
        container: $("#cy"),

        elements: elements,
        layout: {
            name: 'cola',
            directed: false
        },
        style: [

            {
                "selector": "node",
                "style": {
                    'background-image': "data(image)",
                    'height': 40,
                    'width': 40,
                    'background-fit': 'cover',
                    'border-color': '#000',
                    'border-width': 3,
                    'border-opacity': 0.5
                }

            },
            // {
            //     "selector": "node[label]",
            //     "style": {
            //         "label": "data(label)",

            //     }
            // },
            {
                "selector": "edge",
                "style": {
                    
                    'line-color': "data(color)"
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
        //setEdgeDistances();
        elements.forEach(element => {
            if (element.group == 'nodes') {
                cy.$(`#${element.data.id}`).ungrabify();
            }
        });
        setColaLayout();
        setColaLayout();
        setColaLayout();
            
    });
    //var cy = $('#cy').cytoscape('get');

    // });
    // setColaLayout();
    // setColaLayout();
    //based of https://codepen.io/rbogard/details/jOEyWrL

    cy.ready(function () {
        //    tippy.setDefaultProps({followCursor: 'true'});

        cy.elements().forEach(function (element) {
            //console.log(element)
            makePopper(element);
        });

        cy.elements().on('tap', function (event) {
            var currentTapStamp = event.timeStamp;
            var msFromLastTap = currentTapStamp - previousTapStamp;
            console.log()
            if (event.target.isNode()) {
                var node = event.target;
                console.log('tapped ' + node.id());

                cy.fit(node);
                cy.zoom({ level: 1.5, position: { x: node.position('x'), y: node.position('y') } })
                if (msFromLastTap < doubleClickDelayMs) {
                    if (node.selected()) {
                        console.log('selected ' + node.id());
                        GetMoreNodes(node.id());
                        startTime = 0;
                        event.target.tippy.hide();
                    }

                }
                previousTapStamp = currentTapStamp;

            }

            event.target.tippy.show();
            event.target.tippy.setProps({

                animation: 'scale',
                trigger: 'manual',
                interactive: true,
            });

        });

    });

})
var startTime = 0, endTime;
function start() {
    startTime = new Date();
}
function elapsed() {
    endTime = new Date();
    var timeDiff = endTime - startTime; //in ms
    // strip the ms
    timeDiff /= 1000;

    // get seconds 
    console.log(timeDiff);
    //var seconds = Math.round(timeDiff);
    return timeDiff
}
function makePopper(ele) {
    let ref = ele.popperRef(); // used only for positioning
    let dummyDomEle = document.createElement('div');
    ele.tippy = tippy(dummyDomEle, { // tippy options:

        getReferenceClientRect: ref.getBoundingClientRect,

        content: () => {
            let content = document.createElement('div');

            if (ele.isNode()) {
                var twitterLink = '<a href="http://twitter.com/' + ele.data('id') + '">' + ele.data('id') + '</a>';
                if (ele.data('following') >= 1000) {
                    var following = 'Following: ' + ele.data('following') + "+";
                }
                else {
                    var following = 'Following: ' + ele.data('following');
                }
                if (ele.data('followers') >= 1000) {
                    var followers = 'Followers: ' + ele.data('followers') + "+";
                }
                else {
                    var followers = 'Followers: ' + ele.data('followers');
                }
                var image = '<img src="' + ele.data('image') + '" style="float:left;width:50px;height:50px;">';
                //var description = '<i>' + ele.data('description') + '</i>';
                content.innerHTML = image + '&nbsp' + twitterLink + '<br> &nbsp' + following + '<br> &nbsp' + followers;//+ '<p><br>' + description + '</p>'
            }
            else {
                var distance = ele.data('weight');
                content.innerHTML = distance*scale;
            }


            //image + '&nbsp' + twitterLink + '<br> &nbsp' + following +'<br> &nbsp'+ followers+'<p><br>' + description + '</p>';


            return content;
        },
        //trigger: 'manual',
        //interactive:true,
        //interactiveBorder: 30, // probably want manual mode
        onClickOutside(instance, event) {
            // ...
            instance.setProps({


                interactive: false,
            });
            instance.hide();
        },
    });
}
function GetMoreNodes(id) {
    $.ajax({
        type: "GET",
        url: "/graph/AdditionalNodes",
        data: { "twitter_handle": id },
        success: function (data) {
            var objects = JSON.parse(data);
            addedElements = objects;
            var items = cy.add(objects);
            addedElements.forEach(element => {
                if (element.group == 'nodes') {
                    cy.$(`#${element.data.id}`).ungrabify();
                    addedNodes.push(element);
                }
                else {
                    addedEdges.push(element);
                }
            });
            edges = [...edges.concat(addedEdges)]

            setColaLayout();
            setColaLayout();
            items.forEach(function (element) {
                //console.log(element)
                makePopper(element);
            });
            items.on('tap', function (event) {
                var currentTapStamp = event.timeStamp;
                var msFromLastTap = currentTapStamp - previousTapStamp;

                console.log()
                if (event.target.isNode()) {
                    var node = event.target;
                    console.log('tapped ' + node.id());
                    cy.fit(node);
                    cy.zoom({ level: 1.5, position: { x: node.position('x'), y: node.position('y') } })

                    if (msFromLastTap < doubleClickDelayMs) {
                        if (node.selected()) {
                            console.log('selected ' + node.id());
                            GetMoreNodes(node.id());
                            startTime = 0;
                            event.target.tippy.hide();
                        }

                    }
                    previousTapStamp = currentTapStamp;


                }

                event.target.tippy.show();
                event.target.tippy.setProps({

                    animation: 'scale',
                    trigger: 'manual',
                    interactive: true,
                });

            });
            console.log(objects);
        }
    })
}

function toggleNodeLock(lock) {
    ele.forEach(element => {
        if (element.group == 'nodes') {

            var node = cy.$(`#${element.data.id}`)
            if (lock) {
                node.lock();
            }
            else {
                node.unlock();
            }
        }
    });
}

function setGridLayout() {
    //stoggleNodeLock(false);
    var layout = cy.layout({ name: 'grid' }).run();
    layout.on('layoutstop', function () {
        //temporary location
        //setEdgeDistancesQueue();
        setEdgeDistances(edges);
        // toggleNodeLock(true);

    });
}
function setColaLayout() {
    //toggleNodeLock(false);
    var layout = cy.layout({ name: 'cola' }).run();
    layout.on('layoutstop', function () {
        //temporary location
        //setEdgeDistancesQueue();
        //console.log(edges)
        setEdgeDistances(edges);

        // toggleNodeLock(true);

    });
}
function setEulerLayout() {
    //toggleNodeLock(false);
    var layout = cy.layout({ name: 'euler' }).run();
    layout.on('layoutstop', function () {
        //temporary location
        //setEdgeDistancesQueue();
        setEdgeDistances(edges);
        //toggleNodeLock(true);

    });
}

function setEdgeDistances(edges) {
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
            //console.log(el1.id(), angle, el2.id())
            var x = edges[i].data.weight * scale * Math.cos(degrees_to_radians(angle - 90));
            //console.log(x);
            var y = edges[i].data.weight * scale * Math.sin(degrees_to_radians(angle - 90));
            el2.position({ x: x + el1.position('x'), y: y + el1.position('y') });
            //console.log(el1.id(), getAngle(el1.position(), el2.position()), el2.id())
            //console.log(el1.position(), el2.position());
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




