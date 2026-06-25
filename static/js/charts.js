function drawATS(score){

const ctx =
document.getElementById(
"atsChart"
);

new Chart(ctx,{

type:"doughnut",

data:{

labels:["ATS","Remaining"],

datasets:[{

data:[
score,
100-score
]

}]
}

});

}
