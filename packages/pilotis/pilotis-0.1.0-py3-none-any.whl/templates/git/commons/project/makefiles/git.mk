EXPOSED_HELPS += help-git

help-git:
	@echo "##############"
	@echo "# Manage Git #"
	@echo "##############"
	@echo ""
	@echo "Not documented yet"
	@echo ""

prune-branches:
	git remote prune origin
	git branch -vv | grep ': gone]'|  grep -v "\*" | awk '{ print $$1; }' | xargs git branch -d

prune-branches-force:
	git remote prune origin
	git branch -vv | grep ': gone]'|  grep -v "\*" | awk '{ print $$1; }' | xargs git branch -D

pbf: prune-branches-force

post-PR-merge-sync-step-1:
	git switch master
	git pull

post-PR-merge-sync: post-PR-merge-sync-step-1 prune-branches-force

pms: post-PR-merge-sync
