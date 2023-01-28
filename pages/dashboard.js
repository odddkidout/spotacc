import React from 'react'
import styles from '@/styles/Home.module.css'
import { useEffect } from 'react'

const tile = () => {
  return (
    <div>
      
    </div>
  )
}



// fetch data from api/dash and populate every 1 sec




const dashboard = () => {
    const [data, setData] = React.useState(null);

    useEffect(() => {
        const interval = setInterval(() => {
            fetch('http://localhost:3000/api/dash') 
            .then(res => res.json())
            .then(data => setData(data));
        }, 1000);
        return () => clearInterval(interval);
    }, []);
    


  return (
    <div className={styles.container}>
        <div className={styles.item}>
            <h2>Total Accounts</h2>
            <div>
                {data && data.total}
            </div>
        </div>
        <div className={styles.item}>
            <h1>Alive</h1>
            <div>{data && data.alive}</div>
        </div>
        <div className={styles.item}>
            <h1>Locked</h1>
            <div>{(data && data.total)-(data && data.alive)}</div>
        </div>
        <div className={styles.item}>
            <h1>InUse</h1>
            <div>{data && data.inuse}</div>
        </div>        
    </div>
  )
}

export default dashboard
