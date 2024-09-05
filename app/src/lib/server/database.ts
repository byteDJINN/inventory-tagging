import Database from 'better-sqlite3';

const DB_PATH = 'db.sqlite';
const db = new Database(DB_PATH, { verbose: console.log });

db.exec(`
  CREATE TABLE IF NOT EXISTS numbers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value INTEGER NOT NULL
  )
`);

// Function to add a number
export function addNumber(value: number): void {
    const stmt = db.prepare('INSERT INTO numbers (value) VALUES (?)');
    stmt.run(value);
}

// Function to remove a number
export function removeNumber(value: number): void {
    const stmt = db.prepare('DELETE FROM numbers WHERE value = ?');
    stmt.run(value);
}

// Function to get all numbers
export function getAllNumbers(): number[] {
    const stmt = db.prepare('SELECT value FROM numbers');
    return stmt.all().map(row => row.value);
}
