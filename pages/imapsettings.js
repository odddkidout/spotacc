import React from 'react'
import styles from '@/styles/Home.module.css'
const imapsettings = () => {
  return (
    <div className={styles.form}>
      <form action="/api/imaps" method='post'>
        <label className={styles.center}>
            <span>IMAP Username :  </span>
            <input className={styles.item} type="text" name="imapUsername" placeholder="IMAP Username" />
        </label>
        <label className={styles.center}>
            <span>IMAP Password :  </span>
            <input type="Password" name="imapPassword" placeholder="IMAP Password" />
        </label>
        <label className={styles.center}>
            <span>IMAP Host :  </span>
            <input type="text" name="imapHost" placeholder="IMAP Host" />
        </label>
        <input type="submit"></input>
        </form>
    </div>
  )
}

export default imapsettings
