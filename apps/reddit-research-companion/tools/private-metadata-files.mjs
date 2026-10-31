import { lstatSync, existsSync, realpathSync } from 'node:fs';
import path from 'node:path';

/** Refuse repositories (including worktrees/bare repositories) and symlink aliases.
 * This is a local accident barrier, not an OS sandbox or a malicious-user defence.
 */
export function assertOutsideGit(file) {
  const absolute = path.resolve(file);
  for (let current = absolute; ; current = path.dirname(current)) {
    if (existsSync(current)) {
      if (lstatSync(current).isSymbolicLink() || realpathSync(current) !== current) throw new Error('Metadata paths must not use symlinks');
      if (existsSync(path.join(current, '.git')) ||
          (existsSync(path.join(current, 'HEAD')) && existsSync(path.join(current, 'objects')))) throw new Error('Metadata files must be outside every Git worktree/repository');
    }
    if (current === path.dirname(current)) break;
  }
  return absolute;
}

export function assertPrivate(file, directory = false) {
  const stat = lstatSync(file);
  if (stat.isSymbolicLink() || (directory ? !stat.isDirectory() : !stat.isFile()) ||
      (stat.mode & 0o077) !== 0 || (!directory && stat.nlink !== 1) ||
      (process.getuid && stat.uid !== process.getuid())) throw new Error('Metadata storage requires owner-only regular files/directories without hardlinks');
  return stat;
}
