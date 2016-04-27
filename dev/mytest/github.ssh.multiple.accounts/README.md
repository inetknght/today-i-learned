# Access git+ssh Github with multiple keyfiles
1. vim ~/.ssh/config
		Host	github-a
			HostName	github.com
			Port	22
			User	git
			IdentityFile	path-to-identity-file-for-account-a
		Host	github-b
			HostName	github.com
			Port	22
			User	git
			IdentityFile	path-to-identity-file-for-account-b
2. `git clone github-a:inetknght/today-i-learned.git`
3. `git clone github-b:work/work-repository.git`
