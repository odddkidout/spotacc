import {mongoose} from "mongoose";

const connectMongo = async () => {
  try{
      const {connection} = await mongoose.connect(process.env.MONGODB_URI,{
        useNewUrlParser: true,
        useUnifiedTopology: true
      })

      if(connection.readyState==1){
        console.log("MongoDB connected")
      }
      else{
        console.log("MongoDB not connected")
      }
  }
  catch(e){
      return Promise.reject(e)
  }
}

export default connectMongo;
