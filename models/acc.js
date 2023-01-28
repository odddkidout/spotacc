import mongoose from 'mongoose'

/* PetSchema will correspond to a collection in your MongoDB database. */
const AccSchema = new mongoose.Schema({
  email: {
    /* The name of this pet */
    
    type: String,
    unique : true,
    required: [true, 'Please provide an email for this acc'],
    maxlength: [100, 'acc email cant be more than 100 words'],
  },
  pass: {
    /* The owner of this pet */

    type: String,
    required: [true, "Please provide the acc's password"],
    maxlength: [100, "acc pass cannot be more than 100 characters"],
  },
  token: {
    /* The species of your pet */

    type: String,
    required: [true, 'Please specify the token for this acc'],
    maxlength: [200, 'token specified cannot be more than 200 characters'],
  },
  InUse: {
    /* Pet's age, if applicable */

    type: Boolean,
    required: [true, 'Please update status of acc']
  },
  
Working: {
    type: Boolean,
    required: [true, 'Please update if acc is alive or dead']
  
},
})

export default mongoose.models.Acc || mongoose.model('Acc', AccSchema)