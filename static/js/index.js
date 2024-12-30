
import * as d3 from 'd3';  // npm install d3 or yarn add d3
import f3 from 'family-chart';  // npm install family-chart@0.2.1 or yarn add family-chart@0.2.1
import 'family-chart/styles/family-chart.css';

fetch('../templates/data.json')
  .then(res => res.json())
  .then(data => create(data))
  .catch(err => console.error(err))

function create(data) {
  const cont = document.querySelector("div#FamilyChart")  // make sure to create div with id FamilyChart
  const store = f3.createStore({
    data,
    node_separation: 250,
    level_separation: 150
  })
  const svg = f3.createSvg(cont)
  const Card = f3.elements.Card({
    store,
    svg,
    card_dim: {w:220,h:70,text_x:75,text_y:15,img_w:60,img_h:60,img_x:5,img_y:5},
    card_display: [d => `${d.data["first name"]} ${d.data["last name"]}`],
    mini_tree: true,
    link_break: false
  })

  store.setOnUpdate(props => f3.view(store.getTree(), svg, Card, props || {}))
  store.updateTree({initial: true})
}
