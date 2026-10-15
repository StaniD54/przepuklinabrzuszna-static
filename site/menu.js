document.querySelectorAll(".dd>button").forEach(function(b){b.addEventListener("click",function(e){e.stopPropagation();
var d=b.parentNode,o=d.classList.toggle("open");
b.setAttribute("aria-expanded",o);
document.querySelectorAll(".dd.open").forEach(function(x){if(x!==d){x.classList.remove("open");
x.querySelector("button").setAttribute("aria-expanded",false)}})})});
document.addEventListener("click",function(){document.querySelectorAll(".dd.open").forEach(function(x){x.classList.remove("open");
x.querySelector("button").setAttribute("aria-expanded",false)})});

(function(){var bar=document.querySelector(".bar"),cta=document.querySelector(".hero .cta-row");
if(!bar)return;if(!cta||!("IntersectionObserver" in window)){bar.classList.add("show");return}
new IntersectionObserver(function(e){bar.classList.toggle("show",!e[0].isIntersecting)}).observe(cta)})();
