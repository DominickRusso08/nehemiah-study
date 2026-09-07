
const SERMON_IDS = [__SERMON_IDS__];
function startReading() {
  document.getElementById('welcome').style.display = 'none';
  document.getElementById('all-sermons').style.display = 'block';
  attachObserver();
  var el = document.getElementById('sermon-' + SERMON_IDS[0]);
  if (el) el.scrollIntoView({behavior:'smooth'});
}
function jumpTo(id) {
  document.getElementById('welcome').style.display = 'none';
  document.getElementById('all-sermons').style.display = 'block';
  attachObserver();
  var el = document.getElementById('sermon-' + id);
  if (el) setTimeout(function(){ el.scrollIntoView({behavior:'smooth', block:'start'}); }, 30);
  closeSB();
}
function toggleDD(id) {
  var body = document.getElementById(id);
  var btn  = body.previousElementSibling;
  body.classList.toggle('show');
  btn.classList.toggle('open');
}
function toggleSB() {
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('overlay').classList.toggle('show');
}
function closeSB() {
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('overlay').classList.remove('show');
}
function setActive(id) {
  document.querySelectorAll('.sermon-item').forEach(function(el){ el.classList.remove('active'); });
  var item = document.getElementById('item-' + id);
  if (item) { item.classList.add('active'); item.scrollIntoView({block:'nearest', behavior:'smooth'}); }
  var s = document.getElementById('sermon-' + id);
  if (s) {
    var p = s.querySelector('.sd-passage'), t = s.querySelector('.sd-title');
    if (p) document.getElementById('tb-passage').textContent = p.textContent;
    if (t) document.getElementById('tb-title').textContent   = t.textContent;
  }
}
var observerAttached = false;
function attachObserver() {
  if (observerAttached) return;
  observerAttached = true;
  var obs = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if (e.isIntersecting) setActive(e.target.dataset.sermon); });
  }, {rootMargin: '-10% 0px -80% 0px', threshold: 0});
  document.querySelectorAll('.sermon-divider').forEach(function(el){ obs.observe(el); });
}
