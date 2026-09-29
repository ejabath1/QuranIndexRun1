module.exports = {
  testEnvironment: 'node',
  reporters: [
    'default',
    [
      'jest-html-reporter',
      {
        pageTitle: 'QuranIndex Automated Test Report',
        outputPath: 'test-report.html',
        includeFailureMsg: true,
        includeConsoleLog: true
      }
    ]
  ]
};
