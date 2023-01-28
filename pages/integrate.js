import React from 'react'
import styles from '@/styles/Home.module.css'

const integrate = () => {
  return (
    <div className={styles.center}>
        <form action="/api/hello" method='post' className={styles.card}>
            <h2 className={styles.center}>
                Integrate with your MongoDB database
            </h2>
            <label className={styles.center}>
                <span>Mongo Username :  </span>
                <input type="text" name="mongoUsername" placeholder="Mongo Username" />
            </label>
            <label className={styles.center}>
                <span>Mongo Password :  </span>
                <input type="Password" name="mongoPassword" placeholder="Mongo Password" />
            </label>
            <label className={styles.center}>
                <span>Mongo Cluster :  </span>
                <input type="text" name="mongoCluster" placeholder="Mongo Cluster" />
            </label>
            <label className={styles.center}>
                <span>Mongo DB Name :  </span>
                <input type="text" name="databaseName" placeholder="Mongo DB Name" />
            </label>
            <input type="submit"></input>
        
        </form>
    </div>
  )
}

export default integrate
