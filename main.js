// test code writing 

// const variable = 5;

// const array = [ 1, 2 , 3 , 4, 5];
// console.log(array)
// array.forEach((elem, index)=> {
//     array[index] = array[index] * 2
// })

// let newArr = array.map((elem)=> {
//     return elem * 2
// })


// newArr = array.filter((elem, index) => {
//     return elem > 2;
// })

// newArr = array.reduce((prevelem, elem, index) => {
//     return prevelem * elem
// })

// console.log(newArr)

// if ((1 > 5) || (2 < 9) && (9 > 1)) {
//     console.log(true)
// } else {
//     console.log(false)
// }


// const obj = {
//     name: "alice",
//     class : 5,
//     gender: "female"
// }

// for (const item in obj) {
//     console.log(obj[item])
// }

// const arr = [1,2,3,4,'alice', true, 'a']

// const [ _ , ...tony] = arr;
// console.log(tony)

// const newArr = [9, ...tony]

// console.log(newArr)

// const set = new Set([1,2,2,3])

// console.log(set)

// reverse a string

let string = "satyam"
// let newStr = ''
// for (let i = string.length - 1; i >= 0; i--) {
//     newStr = newStr + "" + string[i]
// }

// console.log(newStr)

// two pointer approach ( this won't work since strings are immutable)

// let first = 0, end = string.length-1;

// for(first; first <= end; first++, end--) {
//     let temp = string[first];
//     string[first] = string[end];
//     string[end] = temp;
// }
// console.log(string)

let strArr = string.split("")

let first = 0, end = strArr.length-1;

for(first; first <= end; first++, end--) {
    let temp = strArr[first];
    strArr[first] = strArr[end];
    strArr[end] = temp;
}

string = strArr.join("")
console.log(String(string))

