
var elements = [
    { group: 'nodes', data: { id: 'n0' } },
    { group: 'nodes', data: { id: 'n1' }},
    { group: 'nodes', data: { id: 'n3' }},
    { group: 'nodes', data: { id: 'n2' }},
    { group: 'edges', data: { id: 'e0', source: 'n0', target: 'n1', weight:4 } },
    { group: 'edges', data: { id: 'e1', source: 'n1', target: 'n2', weight:5 } },
    { group: 'edges', data: { id: 'e2', source: 'n0', target: 'n2', weight:5 } }
  ]

$(document).ready(function() {
    var cy = cytoscape({
        container: $("#cy"),
        autolock:false,

        elements:elements,
        layout: {
            name: 'cola',
            
    }
    });
    var layout = cy.layout({name:'cola'}).run();
    layout.on('layoutstop',function() {
        elements.forEach( element => {
            cy.$(`#${element.data.id}`).lock();
        });
    })
    
})






