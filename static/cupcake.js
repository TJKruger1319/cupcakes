const BASE_URL = "http://127.0.0.1:5000/api/cupcakes";
const $section = $('#section');
const $form = $("#form");

async function getCupcakes() {
    //Gets all the cupcakes and adds them to the page
    cupcakes = await axios.get(BASE_URL);
    const length = cupcakes.data.cupcakes.length
    for (let i = 0; i < length; i++) {
        let p = document.createElement("p");
        $(p).text(`Cupcake ${i+1}: Flavor = ${cupcakes.data.cupcakes[i].flavor},
        Size = ${cupcakes.data.cupcakes[i].size}, Rating = ${cupcakes.data.cupcakes[i].rating}`,);
        const img = document.createElement("img");
        img.src = cupcakes.data.cupcakes[i].image;
        $(img).css({"height": "100", "width": "100" })
        $(p).append(img);
        $section.append(p);
    }
}

$form.on("submit", async function(e){
    //Sends the cupcake information to the api
    e.preventDefault();
    const flavor = $("#flavor").val();
    const size = $("#size").val();
    const rating = $("#rating").val();
    const image = $("#image").val();
    await axios.post(BASE_URL, {
        flavor: flavor,
        size: size,
        rating: rating,
        image: image
    });
    $section.empty();
    getCupcakes();
})

getCupcakes();