# GIT

- a revision control system
- a persistent map, keys are hashes and bodies are pieces of content
  - persists content into a blob in the object database
    - /git/objects ... 23/{rest of hash} ... organize content by spreading it out across multiple directories.

### Storage

- Object Database
  - Blob = content (File)
  - Tree = Directory which can contain Trees / Blobs
  - Acts like a file system
  - Stores only unique hashes.
    - multiple files with the same hash will put to the same content in the tree.
    - the tree file tracks the names
  - info / pack directories contain more optimizations

### Branch

- heads folder
 - .git/HEAD ref to the current branch
 - example: refs/heads/main ... the branch it is currently pointed at

 - merge - git creates a commit with 2 parents and moves the head.
 - fast-forward - moving the ref up to another commit without any changes

 - current branch tracks commits
 - when you move to another branch, git updates your working Directory
 - unreachable objects are garbage collected.

 - whole point of merging is that is preserves history. merges never lie.

## Rebase

 - moving commits to another branch without merging
 - the branch moves, the previous branch is garbage collected

 - rebase history is neat, clean and simple. but it is sort of a lie.
 - refactor project history, change the project history.

 - power tool... only use when you know what you are doing.

 - not great with multiple people w/ distributed git... never rebase shared commits

## Tags

 - reference, points to a commit
 - annotation contains metadata and a pointer to a commit
 - tag is just a label and is the hash of the commit (lightweight)
 - tag doesnt move

## Forks / Pull Requests (not a git feature)
 - clone a repo from another account to our own account
   - clone to local
   - add another remmote to the original so we can sync.
   - cannot push to original repo... send pull request
