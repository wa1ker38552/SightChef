function getList() {
    const list = JSON.parse(localStorage.getItem("list"));
    if (list != null) return list;
    return [];
}

function setList(data) {
    localStorage.setItem("list", JSON.stringify(data));
}

function addToList(name, quantity) {
    const list = getList();
    if (name != "" && quantity != "") {
        list.push({"name": name, "quantity": quantity})
    }
    setList(list);
}

function modalClose() {
    addToList(dquery("#ingredientName").value, dquery("#ingredientQuantity").value)
    dquery("#ingredientName").value = "";
    dquery("#ingredientQuantity").value = "";
    loadList();
    animateCloseModal(dquery("#modal"));

}

function removeItem(num, reload) {

    const list = getList();

    if (num < 0 || list == null || num > list.length) 
        return;

    list.splice(num, 1);
    setList(list);
    if (Boolean(reload)) loadList();

}

function loadList() {
    const list = getList();
    if (list == null) {
        return;
    }

    let listItems = "";
    let num = 1;

    list.forEach(element => {
        listItems += `
        <div class="shopping-item" onclick="removeItem(${num - 1}, true)">${element['name']} x${element['quantity']}
        </div>`
        num++;
    });

    document.getElementById("shoppingListItems").innerHTML = listItems;

}

function renderRecipe(item) {
    const e = dcreate("a", "recipe-item", `
        <img src='${item.image}'>
        <h3>${item.name}</h3>
    `)
    e.target = "_blank"
    e.href = item.url
    return e
}

function main() {
    loadList();
    window.onclick = function(e) {
        if (e.target == dquery("#modal")) {
            animateCloseModal(dquery("#modal"))
        }
    }

    const parent = dquery("#searchIngredientsResult")
    const input = dquery("#searchInput")
    input.oninput = function() {
        request("http://localhost:8002/api/search?ingredient="+input.value)
            .then(data => {
                parent.innerHTML = ""
                if (data.success) {
                    for (item of data.data) {
                        parent.append(renderRecipe(item))
                    }
                } else {
                    parent.innerHTML = "<i>No results found</i>"
                }
            })
    }
}

window.onload = main;