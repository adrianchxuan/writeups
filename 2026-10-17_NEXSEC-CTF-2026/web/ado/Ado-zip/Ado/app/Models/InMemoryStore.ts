
export interface StoredUser {
  id: number
  username: string
  password: string
  email: string
  role: 'user' | 'admin'
  recoveryToken: string
}

export interface StoredComment {
  id: number
  userId: number
  postId: number
  body: string
  createdAt: string
}

class InMemoryStore {
  users: StoredUser[] = []
  comments: StoredComment[] = []
  private nextCommentId = 1

  constructor() {
    this.users.push({
      id: 1,
      username: 'admin',
      password: process.env.ADMIN_BOT_PASSWORD, // cred: admin password (set via ADMIN_BOT_PASSWORD)
      email: 'admin@onelastreview.ctf',
      role: 'admin',
      recoveryToken: 'RT-' + Math.random().toString(36).slice(2),
    })

    this.users.push({
      id: 2,
      username: 'Ado',
      password: 'ado123', // cred: Ado's password
      email: 'ado@onelastreview.ctf',
      role: 'user',
      recoveryToken: 'RT-' + Math.random().toString(36).slice(2),
    })

    this.users.push({
      id: 3,
      username: 'Hana',
      password: 'hana123', // cred: Hana's password
      email: 'hana@onelastreview.ctf',
      role: 'user',
      recoveryToken: 'RT-' + Math.random().toString(36).slice(2),
    })

    this.users.push({
      id: 4,
      username: 'Rimi',
      password: 'rimi123', // cred: Rimi's password
      email: 'rimi@onelastreview.ctf',
      role: 'user',
      recoveryToken: 'RT-' + Math.random().toString(36).slice(2),
    })
  }

  findUserById(id: number): StoredUser | undefined {
    return this.users.find((u) => u.id === id)
  }

  findUserByUsername(username: string): StoredUser | undefined {
    const normalizedUsername = username.toLowerCase()
    return this.users.find((user) => user.username.toLowerCase() === normalizedUsername)
  }

  createComment(data: Omit<StoredComment, 'id' | 'createdAt'>): StoredComment {
    const comment: StoredComment = {
      id: this.nextCommentId++,
      createdAt: new Date().toISOString(),
      ...data,
    }
    this.comments.push(comment)
    return comment
  }

  allComments(): StoredComment[] {
    return this.comments
  }
}

export default new InMemoryStore()
