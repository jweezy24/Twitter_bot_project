//scale that will be applied to weights
var scale = 1;

//temporary also in future it will be array of nodes and array of edges
var elements = [
    { group: 'nodes', data: { id: 'n0' , label: 'n0'}, classes: 'center-center' },
    { group: 'nodes', data: { id: 'n1' , label: 'n1'}, classes: 'center-center'},
    { group: 'nodes', data: { id: 'n3' , label: 'n3'}, classes: 'center-center'},
    { group: 'nodes', data: { id: 'n2', label: 'n2' }, classes: 'center-center'},
    { group: 'nodes', data: { id: 'n4', label: 'n4' }, classes: 'center-center', position : {x:0, y:0}},
    { group: 'nodes', data: { id: 'n5', label: 'n5' }, classes: 'center-center'},
    { group: 'nodes', data: { id: 'n6', label: 'n6' }, classes: 'center-center'},
    { group: 'nodes', data: { id: 'n7', label: 'n7' }, classes: 'center-center'},
    { group: 'nodes', data: { id: 'n8', label: 'n8' }, classes: 'center-center', position : {x:10000, y:10000}},
    { group: 'nodes', data: { id: 'n9', label: 'n7' }, classes: 'center-center', },
    { group: 'edges', data: { id: 'e0', source: 'n0', target: 'n1', weight:4 } },
    { group: 'edges', data: { id: 'e1', source: 'n1', target: 'n2', weight:5 } },
    { group: 'edges', data: { id: 'e2', source: 'n0', target: 'n2', weight:5 } },
    { group: 'edges', data: { id: 'e3', source: 'n0', target: 'n4', weight:10 } },
    { group: 'edges', data: { id: 'e4', source: 'n4', target: 'n2', weight:10 } },
    { group: 'edges', data: { id: 'e5', source: 'n3', target: 'n4', weight:10 } },
    { group: 'edges', data: { id: 'e6', source: 'n3', target: 'n5', weight:10 } },
    { group: 'edges', data: { id: 'e7', source: 'n3', target: 'n6', weight:10 } },
    { group: 'edges', data: { id: 'e8', source: 'n2', target: 'n7', weight:10 } },
    { group: 'edges', data: { id: 'e9', source: 'n7', target: 'n8', weight:10 } },
    { group: 'edges', data: { id: 'e10', source: 'n4', target: 'n9', weight:10 } },
    { group: 'edges', data: { id: 'e11', source: 'n4', target: 'n8', weight:10 } },
  ]

$(document).ready(function() {
    var cy = cytoscape({
        container: $("#cy"),
        autolock:false,

        elements:elements,
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
    var layout = cy.layout({name:'cola'}).run();
    layout.on('layoutstop',function() {
        //temporary location
        elements.forEach( element => {
            if (element.group== 'nodes') {
                cy.$(`#${element.data.id}`).lock();
            }
            
            if (element.group == 'edges') {
                var el1 = cy.$(`#${element.data.source}`);
                var el2 = cy.$(`#${element.data.target}`);
            
                //calculate distance and if it is not the same as weight*scale adjust it while keeping angle the same
                
                
                var dist = getDistance(el1.position(), el2.position())
                if (dist !=element.data.weight*scale) {
                    var difference = dist - element.data.weight*scale;
                    //console.log(difference);
                    console.log(el1.id(),getAngle(el1.position(), el2.position()),el2.id() )
                }
            }
        });
    })
    
})

//distance between two points
function getDistance(p1, p2) {
    return Math.sqrt(Math.pow(p2.x - p1.x,2) + Math.pow(p2.y-p1.y,2));
}

function adjustLength(p1, p2) {

}

//angle between two points
function getAngle(p1, p2) {
    // var angle = (Math.atan2(p2.y-p1.y, p2.x-p1.x) * 180) / Math.PI;
    // if (angle < 0) { angle += 360 }
    var p3 = {x:p1.x,y:p1.y-5}
    
    var p12 = getDistance(p2,p1);
    var p13 = getDistance(p3,p1);
    var p23 = getDistance(p3,p2);

    var angle = Math.acos(((Math.pow(p12, 2)) + (Math.pow(p13, 2)) - (Math.pow(p23, 2))) / (2 * p12 * p13)) * 180 / Math.PI;
return angle;
}




