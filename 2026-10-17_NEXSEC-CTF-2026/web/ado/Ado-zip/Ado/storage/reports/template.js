module.exports = {
  generate() {
    const now = new Date()

    const report = {
      title: 'Ado Fan Community Report',
      generatedAt: now.toISOString(),
      summary: 'Placeholder report. Check all stats and notes for details.',
      stats: {
        totalFans: '9.6 million',
        commentsToday: 'TBD',
        topSong: '【Ado】New Genesis / 新時代 (UTA from ONE PIECE FILM RED',
      },
      note: 'This report is generated for internal use only. Please do not share it outside the Ado Fan Community.',
    }

    return JSON.stringify(report, null, 2)
  },
}