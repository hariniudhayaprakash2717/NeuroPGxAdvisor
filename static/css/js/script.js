// =======================================
// NeuroPGx Advisor
// script.js
// =======================================

// Navbar Shadow on Scroll

window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".navbar");

    if (window.scrollY > 50) {

        navbar.style.background = "rgba(2,6,23,0.95)";
        navbar.style.boxShadow = "0 10px 30px rgba(0,0,0,.35)";

    } else {

        navbar.style.background = "rgba(15,23,42,.65)";
        navbar.style.boxShadow = "none";

    }

});

// =======================================
// Hero Button Smooth Scroll
// =======================================

const heroButton = document.querySelector(".hero-btn");

if(heroButton){

heroButton.addEventListener("click",()=>{

    document.querySelector(".form-section").scrollIntoView({

        behavior:"smooth"

    });

});

}

// =======================================
// Predict Button Loading Effect
// =======================================

const form = document.querySelector("form");

const predictBtn = document.querySelector(".predict-btn");

if(form){

form.addEventListener("submit",function(){

    predictBtn.innerHTML =

    '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Patient...';

    predictBtn.disabled = true;

});

}

// =======================================
// Input Focus Animation
// =======================================

const inputs = document.querySelectorAll("input,select");

inputs.forEach(input=>{

input.addEventListener("focus",()=>{

    input.style.boxShadow="0 0 15px rgba(59,130,246,.5)";

});

input.addEventListener("blur",()=>{

    input.style.boxShadow="none";

});

});

// =======================================
// Reveal Animation
// =======================================

const reveals=document.querySelectorAll(

".hero-card,.feature-card,.tech-card,.glass-card,.stat-box,.step"

);

function reveal(){

reveals.forEach(card=>{

const windowHeight=window.innerHeight;

const cardTop=card.getBoundingClientRect().top;

const visible=120;

if(cardTop<windowHeight-visible){

card.style.opacity="1";

card.style.transform="translateY(0px)";

}

});

}

reveals.forEach(card=>{

card.style.opacity="0";

card.style.transform="translateY(70px)";

card.style.transition=".8s ease";

});

window.addEventListener("scroll",reveal);

reveal();

// =======================================
// Floating Hero Cards
// =======================================

const heroCards=document.querySelectorAll(".hero-card");

heroCards.forEach((card,index)=>{

setInterval(()=>{

card.style.transform="translateY(-12px)";

setTimeout(()=>{

card.style.transform="translateY(0px)";

},700);

},3000+(index*500));

});

// =======================================
// Counter Animation
// =======================================

const counters=document.querySelectorAll(".stat-box h2");

counters.forEach(counter=>{

const updateCounter=()=>{

const target=parseInt(counter.innerText);

let count=0;

const speed=Math.ceil(target/60);

const interval=setInterval(()=>{

count+=speed;

if(count>=target){

counter.innerText=target+

(counter.innerText.includes("%")?"%":"+");

clearInterval(interval);

}else{

counter.innerText=count+

(counter.innerText.includes("%")?"%":"+");

}

},30);

};

updateCounter();

});

// =======================================
// Hover Glow
// =======================================

const cards=document.querySelectorAll(

".feature-card,.tech-card,.hero-card"

);

cards.forEach(card=>{

card.addEventListener("mouseenter",()=>{

card.style.boxShadow="0 20px 45px rgba(59,130,246,.35)";

});

card.addEventListener("mouseleave",()=>{

card.style.boxShadow="";

});

});

// =======================================
// Footer Year
// =======================================

const footer=document.querySelector(".footer-content");

if(footer){

const year=document.createElement("p");

year.innerHTML="Current Year : "+new Date().getFullYear();

footer.appendChild(year);

}