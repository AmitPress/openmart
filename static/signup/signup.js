// function validate(event){
//     event.preventDefault()
//     const form = document.forms['signup-form']
//     // fields
//     const fname = form['firstname']
//     const lname = form['lastname']
//     const uname = form['username']
//     const mail = form['email']
//     const pass = form['pass']
//     const cpass = form['confirmpass']
    
// }
const submitbtn = document.forms['signup-form']['signup']

const fname = document.forms['signup-form']['firstname']
const lname = document.forms['signup-form']['lastname']
const uname = document.forms['signup-form']['username']
let firstname = ''
let lastname = ''
let username = ''
fname.addEventListener('keyup', function(event){
    event.stopPropagation()
    firstname = event.target.value
    if(lastname){
        username = firstname +' '+ lastname
    }else{
        username = firstname
    }
    uname.value = username
})

lname.addEventListener('keyup', function(event){
    event.stopPropagation()
    lastname = event.target.value
    if(lastname){
        username = firstname +' '+ lastname
    }else{
        username = firstname
    }
    uname.value = username
})



const mail = document.forms['signup-form']['email']

mail.addEventListener('keyup', function(event){
    event.stopPropagation()
    let construct = event.target.value
    let re = /\w+@\w+\.+\w+/g
    const result = re.test(construct)
    if(result){
        mail.style.border="2px solid green"
    }else{
        mail.style.border="2px solid red"
    }
    mail.addEventListener('blur', function(event){
        event.stopPropagation()
        if(result){
            mail.style.border="1px solid #ced4da"
        }else{
            mail.style.border="2px solid red"
        }
    })
})


// authentication
const pass = document.forms['signup-form']['pass']
const confirmpass = document.forms['signup-form']['confirmpass']

confirmpass.addEventListener('keyup', function(event){
    event.stopPropagation()
    const result = pass.value != event.target.value
    if(result){
        confirmpass.style.border = confirmpass.style.border="2px solid red"
    }else{
        confirmpass.style.border="1px solid green"
    }
    confirmpass.addEventListener('blur', function(event){
        event.stopPropagation()
        if(result){
            confirmpass.style.border="2px solid red"
        }else{
            confirmpass.style.border="1px solid #ced4da"
        }
    })
})