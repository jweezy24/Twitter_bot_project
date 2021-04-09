//scale that will be applied to weights
var scale = 1;

//temporary also in future it will be array of nodes and array of edges
var elements = [
    { group: 'nodes', data: { id: 'n0' , label: 'n0', "visited": false}, classes: 'center-center' },
    { group: 'nodes', data: { id: 'n1' , label: 'n1', "visited": false}, classes: 'center-center'},
    { group: 'nodes', data: { id: 'n3' , label: 'n3', "visited": false}, classes: 'center-center'},
    { group: 'nodes', data: { id: 'n2', label: 'n2' , "visited": false}, classes: 'center-center'},
    { group: 'nodes', data: { id: 'n4', label: 'n4' , "visited": false}, classes: 'center-center', },
    { group: 'nodes', data: { id: 'n5', label: 'n5' , "visited": false}, classes: 'center-center'},
    { group: 'nodes', data: { id: 'n6', label: 'n6' , "visited": false}, classes: 'center-center'},
    { group: 'nodes', data: { id: 'n7', label: 'n7' , "visited": false}, classes: 'center-center'},
    { group: 'nodes', data: { id: 'n8', label: 'n8' , "visited": false}, classes: 'center-center', },
    { group: 'nodes', data: { id: 'n9', label: 'n7' , "visited": false}, classes: 'center-center', },
    { group: 'edges', data: { id: 'e0', source: 'n0', target: 'n1', weight:100 , "visited": false} },
    //{ group: 'edges', data: { id: 'e1', source: 'n1', target: 'n2', weight:5 , "visited": false} },
    { group: 'edges', data: { id: 'e2', source: 'n0', target: 'n2', weight:150 , "visited": false} },
    { group: 'edges', data: { id: 'e3', source: 'n0', target: 'n4', weight:150 , "visited": false} },
    { group: 'edges', data: { id: 'e4', source: 'n4', target: 'n2', weight:100 , "visited": false} },
    { group: 'edges', data: { id: 'e5', source: 'n3', target: 'n4', weight:100, "visited": false } },
    { group: 'edges', data: { id: 'e6', source: 'n3', target: 'n5', weight:100 , "visited": false} },
    { group: 'edges', data: { id: 'e7', source: 'n3', target: 'n6', weight:100 , "visited": false} },
    { group: 'edges', data: { id: 'e8', source: 'n2', target: 'n7', weight:100 , "visited": false} },
    { group: 'edges', data: { id: 'e9', source: 'n7', target: 'n8', weight:100 , "visited": false} },
    { group: 'edges', data: { id: 'e10', source: 'n4', target: 'n9', weight:300 , "visited": false} },
    { group: 'edges', data: { id: 'e11', source: 'n4', target: 'n8', weight:200 , "visited": false} },
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
        
        for(let i =0; i <elements.length;i++) {

        
            
            
            if (elements[i].group == 'edges') {
                
                var el1 = cy.$(`#${elements[i].data.source}`);
                var el2 = cy.$(`#${elements[i].data.target}`);
                
                if (el2.data('visited')==true) {
                    
                    continue;
                }
                //calculate distance and if it is not the same as weight*scale adjust it while keeping angle the same
                
                
                var dist = getDistance(el1.position(), el2.position())
                if (dist !=elements[i].data.weight*scale) {
                    var difference = dist - elements[i].data.weight*scale;
                    //console.log(difference);
                    var angle = getAngle(el1.position(), el2.position());
                    console.log(el1.id(),angle,el2.id())
                    var x = elements[i].data.weight*scale*Math.cos(degrees_to_radians(angle-90));
                    console.log(x);
                    var y = elements[i].data.weight*scale* Math.sin(degrees_to_radians(angle-90));
                    el2.position({x:x+el1.position('x'), y:y+el1.position('y')});
                    console.log(el1.id(),getAngle(el1.position(), el2.position()),el2.id())
                    console.log(el1.position(), el2.position());
                    el2.data('visited', true);
                    
                }
            }
        }
        elements.forEach(element => {
            if (element.group== 'nodes') {
                cy.$(`#${element.data.id}`).lock();
            }
        });

    })
    
})

function degrees_to_radians(degree) {
    
    return degree*(Math.PI/180);
}

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
    if (p2.x <p1.x) {
        angle = 360-angle;
    }
return angle;
}




