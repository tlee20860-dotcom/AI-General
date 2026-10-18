## 修改目標: `.github/workflows/apply-patch.yml`

<<<<<<< REGEX
jobs:\n  apply:\n    runs-on: ubuntu-latest
=======
jobs:
  apply:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      workflows: write
>>>>>>> NEW