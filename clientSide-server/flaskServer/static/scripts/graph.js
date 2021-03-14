//scale that will be applied to weights
var scale = 1;

//temporary also in future it will be array of nodes and array of edges
var elements = [
    { group: 'nodes', data: { id: 'n0' , label: 'n0'}, classes: 'center-center' },
    { group: 'nodes', data: { id: 'n1' , label: 'n1'}, classes: 'center-center'},
    { group: 'nodes', data: { id: 'n3' , label: 'n3'}, classes: 'center-center'},
    { group: 'nodes', data: { id: 'n2', label: 'n2' }, classes: 'center-center'},
    { group: 'edges', data: { id: 'e0', source: 'n0', target: 'n1', weight:4 } },
    { group: 'edges', data: { id: 'e1', source: 'n1', target: 'n2', weight:5 } },
    { group: 'edges', data: { id: 'e2', source: 'n0', target: 'n2', weight:5 } }
  ]

$(document).ready(function() {
    var cy = cytoscape({
        container: $("#cy"),
        autolock:false,

        elements:elements,
        // layout: {
        //     name: 'cola',
            
        // },
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




