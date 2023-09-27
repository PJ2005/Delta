const laptops = [
    {
        id: 1,
        model: "Education",
        basePrice: 20000,
        ram: [
            {size: 4, price: 2000},
            {size: 8, price: 4000}
        ],
        storage: [
            {size: 256, price: 2000},
            {size: 512, price: 3000}
        ],
        processor: [
            {type: "i3", price: 5000},
            {type: "i5", price: 7000}
        ]
    },
    {
        id: 2,
        model: "College",
        basePrice: 30000,
        ram: [
            {size: 8, price:4000},
            {size: 16, price: 6000}
        ],
        storage: [
            {size: 256, price: 2000},
            {size: 512, price: 3000},
            {size: 1, price: 5000}
        ],
        processor: [
            {type: "i3", price: 5000},
            {type: "i5", price: 8000},
            {type: "i7", price: 10000}
        ]
    },
    {
        id: 3,
        model: "Work",
        basePrice: 40000,
        ram: [
            {size: 8, price:4000},
            {size: 16, price: 6000}
        ],
        storage: [
            {size: 256, price: 2000},
            {size: 512, price: 3000},
            {size: 1, price: 5000},
            {size: 2, price: 7000}
        ],
        processor: [
            {type: "i5", price: 8000},
            {type: "i7", price: 10000},
        ]
    },
    {
        id: 4,
        model: "Gaming",
        basePrice: 50000,
        ram: [
            {size: 8, price:4000},
            {size: 16, price: 6000},
            {size: 32, price: 10000}
        ],
        storage: [
            {size: 256, price: 4000},
            {size: 512, price: 6000},
            {size: 1, price: 8000},
            {size: 2, price: 10000}
        ],
        processor: [
            {type: "i5", price: 10000},
            {type: "i7", price: 12000},
            {type: "i9", price: 15000}
        ]
    }
]

function addToCart(laptopID, RAMSize, storageSize, processorType){
    let dic = {
        orderID : count += 1,
        lapID : laptopID,
        RAM : RAMSize,
        storage : storageSize,
        processor : processorType
    };

    cart.push(dic);
};


function removeFromCart(inp){
    for (let i of cart){
        console.log(i);
        if (i.orderID === Number(inp)){
            const index = cart.indexOf(i)
            if (index > -1){
                    cart.splice(i, 1);
            }
            else {
                console.log("Cart is empty");
            }
        }
        else{
            console.log("The given orderID doesn't exist or the cart is empty");
        }
    }
};


function calculateTotal(){
    for (var i = 0; i < cart.length; i++){
        let tempID = Number(cart[i].lapID);
        let tempRAM = Number(cart[i].RAM);
        let tempStorage = Number(cart[i].storage);
        let tempProcess = cart[i].processor;
        console.log(tempID);
        price += laptops[tempID - 1].basePrice;

        let temp = laptops[tempID - 1].ram;
        for (var j of temp){
            if (j.size === tempRAM){
                price += j.price;
            }

        let temp = laptops[tempID - 1].storage;
        for (var j of temp){
            if (j.size === tempStorage){
                price += j.price;
            }
        
        let temp = laptops[tempID - 1].processor;
        for (var j of temp){
            if (j.type === tempProcess){
                price += j.price;
            }
        }
        }
        }
    }
}

let cart = [];
let count = 0;
let price = 0;


console.log(" 1 - To view the list of items available \n 2 - To add items to the cart \n 3 - To remove an item from a cart \n 4 - To calculate total price \n 5 - To exit the program");

while (true){
    let choice = Number(prompt("Enter the choice: "));
    if (choice === 1){
        console.log(`List of items available are \n ${laptops}`);
    }

    else if (choice === 2){
        let laptopID = prompt("Enter laptop ID: ");
        let RAMSize = prompt("Enter RAM Size: ");
        let storageSize = prompt("Enter storage size: ");
        let processorType = prompt("Enter processor type: ");
        addToCart(laptopID, RAMSize, storageSize, processorType);
        console.log(`Items in the cart are \n ${cart}`);
    }

    else if (choice === 3){
        console.log(cart);
        let inp = prompt("Enter the orderID of the item u want to remove from cart: ");
        removeFromCart(inp);
        console.log(`Cart after removing items is \n ${cart}`);
    }

    else if (choice === 4){
        calculateTotal();
        console.log(`The total price of items in the cart is ${price}`);
    }

    else{
        console.log("You have succesfully exited the program");
        break;
    }
};