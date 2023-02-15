import Head from 'next/head'
import Image from 'next/image'
import Link from 'next/link'
import styles from '../styles/Home.module.css'
import { Inter } from '@next/font/google'


const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  return (
    <>
      <Head>
        <title>Spotify Account manager</title>
        <meta name="description" content="Made by Odddkidout" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <main className={styles.main}>
        
        <div className={styles.center}>
          <h1 className={styles.center}>
            Spotify Account manager
          </h1>
        </div>

        <div className={styles.grid}>
          <Link
            href="/dashboard"
            className={styles.card}
          >
            <h2 className={inter.className}>
              Dashboard <span>-&gt;</span>
            </h2>
            <p className={inter.className}>
              Dashboard for analytics and account management.
            </p>
          </Link>

          <Link
            href="/upload"
            className={styles.card}
          >
            <h2 className={inter.className}>
              Upload <span>-&gt;</span>
            </h2>
            <p className={inter.className}>
              Upload accounts to the database.
            </p>
          </Link>

          <Link
            href="/imapsettings"
            className={styles.card}
          >
            <h2 className={inter.className}>
              IMAP Settings <span>-&gt;</span>
            </h2>
            <p className={inter.className}>
              Setup IMAP server Logins.
            </p>
          </Link>
          <Link href="/integrate" className={styles.card}>
          
            <h2 className={inter.className}>
              Database Settings <span>-&gt;</span>
            </h2>
            <p className={inter.className}>
              Intergrate database and deploy to the cloud on mongodb .
            </p>
          
          </Link>
        </div>
      </main>
    </>
  )
}
