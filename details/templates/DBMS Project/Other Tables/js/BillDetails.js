var table = document.querySelector('table'), 
    table_meta_container = table.querySelector('thead'), 
    table_data_container = table.querySelector('tbody'),
    data = [
  { 'billID': 'Scooby', 'billDate': 'Doo', 'custID': 1969, 'total': 12}, 
  { 'billID': 'Yogi', 'billDate': 'Bear', 'custID': 1958, 'total':  12}, 
  { 'billID': 'Tom', 'billDate': 'Cat', 'custID': 1940, 'total':  12}, 
  { 'billID': 'Jerry', 'billDate': 'Mouse', 'custID': 1940, 'total': 12 }, 
  { 'billID': 'Fred', 'billDate': 'Flintstone', 'custID': 1960, 'total': 12 }
], n = data.length;

var createTable = function(src) {
  var frag = document.createDocumentFragment(), 
      curr_item, curr_p;
  
  for(var i = 0; i < n; i++) {
    curr_item = document.createElement('tr');
    curr_item.classList.add(((i%2 === 0)?'odd':'even'));
    data[i].el = curr_item;
    
    for(var p in data[i]) {
      if(p !== 'el') {
        curr_p = document.createElement('td');
        curr_p.classList.add('prop__value');
        curr_p.dataset.propName = p;
        curr_p.textContent = data[i][p];
        curr_item.appendChild(curr_p)
      }
    }
    
    frag.appendChild(curr_item);
  }
  
  table_data_container.appendChild(frag);
};

var sortTable = function(entries, type, dir) {  
  entries.sort(function(a, b) { 
    if(a[type] < b[type]) return -dir;
    if(a[type] > b[type]) return dir;
    return 0;
  });
  
  table.dataset.sortBy = type;
  
  for(var i = 0; i < n; i++) {
    entries[i].el.style.order = i + 1;
    
    if((i%2 === 0 && entries[i].el.classList.contains('even')) || 
       (i%2 !== 0 && entries[i].el.classList.contains('odd'))) {
      entries[i].el.classList.toggle('odd');
      entries[i].el.classList.toggle('even');
    }
  }
};

createTable(data);

table_meta_container.addEventListener('click', function(e) {
  var t = e.target;
  
  if(t.classList.contains('prop__name')) {
    if(!t.dataset.dir) { t.dataset.dir = 1; }
    else { t.dataset.dir *= -1; }
    
    sortTable(data, t.dataset.propName, t.dataset.dir);
  }
}, false);