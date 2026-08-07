

# FreshFlow - Git Merge Debugging Notes

## Problem

Image upload was still failing after merging **PR #32**.

PR branch:

```text
fix/product-image-uploads-404-2665077497828404722
```

I believed the fix was merged, but the application still had the same bug.

---

# Step 1 - Verify current branch

```bash
git checkout main
git status
```

Output:

```text
On branch main
Your branch is up to date with 'origin/main'
```

Meaning:

* Working on `main`
* No local changes

---

# Step 2 - Pull latest code

```bash
git pull origin main
```

Output:

```text
Already up to date.
```

Initially this looked correct.

---

# Step 3 - Check commit history

```bash
git log --oneline --max-count=5
```

Output:

```text
10128a9 Merge pull request #32
408c02c fix: resolve product image upload failure...
```

This confirmed:

* PR #32 was merged.
* Local `main` matched GitHub `main`.

At this point it looked like everything was correct.

---

# Step 4 - Mistake

I manually tried:

```bash
git merge origin/fix/product-image-uploads-404-2665077497828404722
```

Git created another merge commit.

Result:

```text
Your branch is ahead of 'origin/main'
```

This happened because I merged an already merged branch.

---

# Step 5 - Recover

Instead of pushing the duplicate merge:

```bash
git reset --hard origin/main
```

Result:

```text
HEAD is now at 10128a9
```

Local repository became identical to GitHub.

---

# Step 6 - Investigate instead of guessing

Instead of merging again, compare the branch with `main`.

```bash
git log main..origin/fix/product-image-uploads-404-2665077497828404722
```

Output:

```text
55f822d fix: resolve product image upload failure...
```

This proved something important:

**There was still one commit on the feature branch that was not in `main`.**

---

# Step 7 - Verify differences

```bash
git diff 10128a9..55f822d
```

Found these missing changes:

## api/boot.ts

Old

```ts
resolve(process.cwd(), "uploads")
```

New

```ts
resolve(process.cwd(), "uploads/products")
```

---

Old API

```ts
POST /api/uploads/products
```

New API

```ts
POST /api/products/upload
```

---

## AddProduct.tsx

Old

```ts
fetch("/api/uploads/products")
```

New

```ts
fetch("/api/products/upload")
```

---

These changes were **not present** in `main`.

---

# Root Cause

PR #32 merged commit

```
408c02c
```

Later another commit was added to the same branch

```
55f822d
```

That second commit never reached `main`.

Therefore:

* PR #32 was merged.
* Feature branch received another commit afterward.
* `main` was missing that latest commit.

---

# Lesson Learned

Never assume:

> "PR is merged = latest branch code is merged."

Always verify.

---

# Useful Git Commands

### Check current branch

```bash
git status
```

---

### Pull latest code

```bash
git pull origin main
```

---

### View recent commits

```bash
git log --oneline
```

---

### Compare branch with main

```bash
git log main..origin/<branch>
```

If commits appear:

✅ Branch contains commits missing from `main`.

---

### Compare code

```bash
git diff main..origin/<branch>
```

Shows exactly what is missing.

---

### Show one commit

```bash
git show <commit>
```

Useful to inspect changes before merging.

---

### Remove accidental merge

```bash
git reset --hard origin/main
```

Restores local repository to match GitHub.

---

### Apply one missing commit

```bash
git cherry-pick <commit>
```

Best when only a single commit is missing.

---

# Interview Explanation

> While debugging a production issue, I noticed the application still had a bug even though the related Pull Request had already been merged. Instead of assuming the deployment was wrong, I compared the feature branch with `main` using `git log main..origin/<branch>` and `git diff`. That investigation showed the feature branch had received an additional commit after the Pull Request was merged, so `main` was missing the latest fix. I avoided creating duplicate merge commits, reset an accidental local merge, verified the missing changes, and then planned to integrate the missing commit correctly. This reinforced the importance of verifying commit history instead of assuming a merged PR always contains the latest branch changes.

---

## Key DevOps Learning

**A merged Pull Request does not necessarily mean the feature branch is fully merged forever.** If new commits are pushed to that branch after the PR merge, those commits are **not automatically added to `main`**. Always verify branch differences before concluding that the latest fix has been deployed.
