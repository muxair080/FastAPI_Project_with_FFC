
main_div = document.getElementById("Main");

async function get_data(){
    URL = "http://127.0.0.1:8000/posts"
    response = await fetch(URL)
    data = await data.json()
    console.log("Data======> : ",data)
}

get_data();

