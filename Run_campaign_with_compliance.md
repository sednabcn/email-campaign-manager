Run echo "🔒 Running Integrated Campaign with Compliance..."
🔒 Running Integrated Campaign with Compliance...
📋 Configuration:
  - Dry Run: false
  - Daily Limit: 50
  - Per-Domain Limit: 5

📤 LIVE MODE: Executing actual campaign

Executing: python utils/integrated_runner.py --contacts contacts --scheduled scheduled-campaigns --tracking tracking --templates campaign-templates --alerts alerts@modelphysmat.com

================================================================================
INTEGRATED EMAIL CAMPAIGN SYSTEM
================================================================================
Start time: 2025-10-14 16:29:16.914931
Mode: LIVE
Contacts dir: contacts
Scheduled dir: scheduled-campaigns
Tracking dir: tracking
Templates dir: campaign-templates
Alerts email: alerts@modelphysmat.com
Tracking directory ready: tracking

🔍 Validating system setup...
✅ Found contacts directory: contacts
✅ Found scheduled directory: scheduled-campaigns
✅ Found tracking directory: tracking
✅ Found templates directory: campaign-templates

📂 Checking utils directory: /home/runner/work/email-campaign-manager/email-campaign-manager/utils
✅ Found data_loader.py
✅ Found docx_parser.py
✅ Found generate_summary.py
✅ Found 4 contact files in contacts
✅ Found 2 campaign files in scheduled-campaigns
✅ requests library available

================================================================================
EXECUTION COMPLETE
================================================================================
Contacts loaded: 0 (WARNING)
Mode: LIVE

Generated files in tracking:
  - .gitkeep (0 bytes)
  - campaign_summary.md (1,129 bytes)
  - rate_limits.json (142 bytes)
  - unsubscribed.json (302 bytes)

Log files generated:
  - campaign_execution.log (425 bytes)

Final Status: PARTIAL
Completed: 2025-10-14 16:29:33.804339

Exit code: 0
✅ Campaign execution completed successfully

======LOGS====
2025-10-14T16:28:46.5461089Z Current runner version: '2.328.0'
2025-10-14T16:28:46.5492172Z ##[group]Runner Image Provisioner
2025-10-14T16:28:46.5493384Z Hosted Compute Agent
2025-10-14T16:28:46.5494526Z Version: 20250912.392
2025-10-14T16:28:46.5495476Z Commit: d921fda672a98b64f4f82364647e2f10b2267d0b
2025-10-14T16:28:46.5496660Z Build Date: 2025-09-12T15:23:14Z
2025-10-14T16:28:46.5497621Z ##[endgroup]
2025-10-14T16:28:46.5499074Z ##[group]Operating System
2025-10-14T16:28:46.5499931Z Ubuntu
2025-10-14T16:28:46.5500682Z 24.04.3
2025-10-14T16:28:46.5501558Z LTS
2025-10-14T16:28:46.5502256Z ##[endgroup]
2025-10-14T16:28:46.5503069Z ##[group]Runner Image
2025-10-14T16:28:46.5504268Z Image: ubuntu-24.04
2025-10-14T16:28:46.5505109Z Version: 20250929.60.1
2025-10-14T16:28:46.5506809Z Included Software: https://github.com/actions/runner-images/blob/ubuntu24/20250929.60/images/ubuntu/Ubuntu2404-Readme.md
2025-10-14T16:28:46.5509537Z Image Release: https://github.com/actions/runner-images/releases/tag/ubuntu24%2F20250929.60
2025-10-14T16:28:46.5511342Z ##[endgroup]
2025-10-14T16:28:46.5513404Z ##[group]GITHUB_TOKEN Permissions
2025-10-14T16:28:46.5516427Z Actions: write
2025-10-14T16:28:46.5517291Z Contents: read
2025-10-14T16:28:46.5518126Z Issues: write
2025-10-14T16:28:46.5518976Z Metadata: read
2025-10-14T16:28:46.5519727Z Packages: write
2025-10-14T16:28:46.5520554Z ##[endgroup]
2025-10-14T16:28:46.5523730Z Secret source: Actions
2025-10-14T16:28:46.5525259Z Prepare workflow directory
2025-10-14T16:28:46.6060799Z Prepare all required actions
2025-10-14T16:28:46.6115468Z Getting action download info
2025-10-14T16:28:46.8936956Z Download action repository 'actions/checkout@v4' (SHA:08eba0b27e820071cde6df949e0beb9ba4906955)
2025-10-14T16:28:47.0868043Z Download action repository 'actions/setup-python@v4' (SHA:7f4fc3e22c37d6ff65e88745f38bd3157c663f7c)
2025-10-14T16:28:47.2559111Z Download action repository 'actions/upload-artifact@v4' (SHA:ea165f8d65b6e75b540449e92b4886f43607fa02)
2025-10-14T16:28:47.4607219Z Complete job name: enhanced-validation-and-prepare
2025-10-14T16:28:47.5506472Z ##[group]Run actions/checkout@v4
2025-10-14T16:28:47.5507778Z with:
2025-10-14T16:28:47.5508527Z   fetch-depth: 1
2025-10-14T16:28:47.5509445Z   repository: sednabcn/email-campaign-manager
2025-10-14T16:28:47.5510815Z   token: ***
2025-10-14T16:28:47.5511575Z   ssh-strict: true
2025-10-14T16:28:47.5512374Z   ssh-user: git
2025-10-14T16:28:47.5513185Z   persist-credentials: true
2025-10-14T16:28:47.5514370Z   clean: true
2025-10-14T16:28:47.5515209Z   sparse-checkout-cone-mode: true
2025-10-14T16:28:47.5516206Z   fetch-tags: false
2025-10-14T16:28:47.5517046Z   show-progress: true
2025-10-14T16:28:47.5517864Z   lfs: false
2025-10-14T16:28:47.5518625Z   submodules: false
2025-10-14T16:28:47.5519447Z   set-safe-directory: true
2025-10-14T16:28:47.5520593Z env:
2025-10-14T16:28:47.5521380Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:28:47.5522482Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:28:47.5523571Z   PYTHON_VERSION: 3.11
2025-10-14T16:28:47.5524622Z   PRODUCTION_MODE: true
2025-10-14T16:28:47.5525489Z   TRACKING_DIR: tracking
2025-10-14T16:28:47.5526394Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:28:47.5527427Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:28:47.5528467Z   CONTACTS_DIR: contacts
2025-10-14T16:28:47.5529341Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:28:47.5530213Z ##[endgroup]
2025-10-14T16:28:47.6747175Z Syncing repository: sednabcn/email-campaign-manager
2025-10-14T16:28:47.6751242Z ##[group]Getting Git version info
2025-10-14T16:28:47.6753939Z Working directory is '/home/runner/work/email-campaign-manager/email-campaign-manager'
2025-10-14T16:28:47.6757855Z [command]/usr/bin/git version
2025-10-14T16:28:47.6836802Z git version 2.51.0
2025-10-14T16:28:47.6875501Z ##[endgroup]
2025-10-14T16:28:47.6892177Z Temporarily overriding HOME='/home/runner/work/_temp/4b34446f-689a-4e0d-9e2e-2bc791c2288f' before making global git config changes
2025-10-14T16:28:47.6895504Z Adding repository directory to the temporary git global config as a safe directory
2025-10-14T16:28:47.6910054Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/email-campaign-manager/email-campaign-manager
2025-10-14T16:28:47.6954897Z Deleting the contents of '/home/runner/work/email-campaign-manager/email-campaign-manager'
2025-10-14T16:28:47.6959265Z ##[group]Initializing the repository
2025-10-14T16:28:47.6964881Z [command]/usr/bin/git init /home/runner/work/email-campaign-manager/email-campaign-manager
2025-10-14T16:28:47.7136805Z hint: Using 'master' as the name for the initial branch. This default branch name
2025-10-14T16:28:47.7141395Z hint: is subject to change. To configure the initial branch name to use in all
2025-10-14T16:28:47.7144588Z hint: of your new repositories, which will suppress this warning, call:
2025-10-14T16:28:47.7146836Z hint:
2025-10-14T16:28:47.7148339Z hint: 	git config --global init.defaultBranch <name>
2025-10-14T16:28:47.7150297Z hint:
2025-10-14T16:28:47.7152122Z hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
2025-10-14T16:28:47.7155281Z hint: 'development'. The just-created branch can be renamed via this command:
2025-10-14T16:28:47.7157659Z hint:
2025-10-14T16:28:47.7158880Z hint: 	git branch -m <name>
2025-10-14T16:28:47.7160322Z hint:
2025-10-14T16:28:47.7162268Z hint: Disable this message with "git config set advice.defaultBranchName false"
2025-10-14T16:28:47.7166344Z Initialized empty Git repository in /home/runner/work/email-campaign-manager/email-campaign-manager/.git/
2025-10-14T16:28:47.7172437Z [command]/usr/bin/git remote add origin https://github.com/sednabcn/email-campaign-manager
2025-10-14T16:28:47.7216502Z ##[endgroup]
2025-10-14T16:28:47.7218906Z ##[group]Disabling automatic garbage collection
2025-10-14T16:28:47.7223795Z [command]/usr/bin/git config --local gc.auto 0
2025-10-14T16:28:47.7260535Z ##[endgroup]
2025-10-14T16:28:47.7262658Z ##[group]Setting up auth
2025-10-14T16:28:47.7270248Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2025-10-14T16:28:47.7303640Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2025-10-14T16:28:48.1613617Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2025-10-14T16:28:48.1642565Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2025-10-14T16:28:48.1860834Z [command]/usr/bin/git config --local http.https://github.com/.extraheader AUTHORIZATION: basic ***
2025-10-14T16:28:48.1895296Z ##[endgroup]
2025-10-14T16:28:48.1896281Z ##[group]Fetching the repository
2025-10-14T16:28:48.1903435Z [command]/usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +35c23aa34dddee12a217d3561f5b3a8e7fd1063f:refs/remotes/origin/master
2025-10-14T16:28:48.4134732Z From https://github.com/sednabcn/email-campaign-manager
2025-10-14T16:28:48.4135726Z  * [new ref]         35c23aa34dddee12a217d3561f5b3a8e7fd1063f -> origin/master
2025-10-14T16:28:48.4164855Z ##[endgroup]
2025-10-14T16:28:48.4165715Z ##[group]Determining the checkout info
2025-10-14T16:28:48.4166839Z ##[endgroup]
2025-10-14T16:28:48.4172076Z [command]/usr/bin/git sparse-checkout disable
2025-10-14T16:28:48.4210790Z [command]/usr/bin/git config --local --unset-all extensions.worktreeConfig
2025-10-14T16:28:48.4239391Z ##[group]Checking out the ref
2025-10-14T16:28:48.4243521Z [command]/usr/bin/git checkout --progress --force -B master refs/remotes/origin/master
2025-10-14T16:28:48.4392849Z Reset branch 'master'
2025-10-14T16:28:48.4395541Z branch 'master' set up to track 'origin/master'.
2025-10-14T16:28:48.4401919Z ##[endgroup]
2025-10-14T16:28:48.4435716Z [command]/usr/bin/git log -1 --format=%H
2025-10-14T16:28:48.4456675Z 35c23aa34dddee12a217d3561f5b3a8e7fd1063f
2025-10-14T16:28:48.4685617Z ##[group]Run actions/setup-python@v4
2025-10-14T16:28:48.4686185Z with:
2025-10-14T16:28:48.4686622Z   python-version: 3.11
2025-10-14T16:28:48.4687077Z   cache: pip
2025-10-14T16:28:48.4687516Z   check-latest: false
2025-10-14T16:28:48.4688135Z   token: ***
2025-10-14T16:28:48.4688587Z   update-environment: true
2025-10-14T16:28:48.4689092Z   allow-prereleases: false
2025-10-14T16:28:48.4689565Z env:
2025-10-14T16:28:48.4690007Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:28:48.4690576Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:28:48.4691115Z   PYTHON_VERSION: 3.11
2025-10-14T16:28:48.4691581Z   PRODUCTION_MODE: true
2025-10-14T16:28:48.4692054Z   TRACKING_DIR: tracking
2025-10-14T16:28:48.4692556Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:28:48.4693101Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:28:48.4693615Z   CONTACTS_DIR: contacts
2025-10-14T16:28:48.4694279Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:28:48.4694777Z ##[endgroup]
2025-10-14T16:28:48.6350862Z ##[group]Installed versions
2025-10-14T16:28:48.6465974Z Successfully set up CPython (3.11.13)
2025-10-14T16:28:48.6467556Z ##[endgroup]
2025-10-14T16:28:48.7266449Z [command]/opt/hostedtoolcache/Python/3.11.13/x64/bin/pip cache dir
2025-10-14T16:28:51.4899266Z /home/runner/.cache/pip
2025-10-14T16:28:51.6255052Z Cache hit for: setup-python-Linux-24.04-Ubuntu-python-3.11.13-pip-c80903bf1241d08be2427b1f1bf80294abd0502ad51eabb583841695e89ba76d
2025-10-14T16:28:52.0290429Z Received 70256460 of 70256460 (100.0%), 179.1 MBs/sec
2025-10-14T16:28:52.0291602Z Cache Size: ~67 MB (70256460 B)
2025-10-14T16:28:52.0405123Z [command]/usr/bin/tar -xf /home/runner/work/_temp/26293bde-a4ae-4148-bb59-41ef895bdde4/cache.tzst -P -C /home/runner/work/email-campaign-manager/email-campaign-manager --use-compress-program unzstd
2025-10-14T16:28:52.1811286Z Cache restored successfully
2025-10-14T16:28:52.1948521Z Cache restored from key: setup-python-Linux-24.04-Ubuntu-python-3.11.13-pip-c80903bf1241d08be2427b1f1bf80294abd0502ad51eabb583841695e89ba76d
2025-10-14T16:28:52.2101432Z ##[group]Run echo "Installing Python dependencies for enhanced production system..."
2025-10-14T16:28:52.2102089Z [36;1mecho "Installing Python dependencies for enhanced production system..."[0m
2025-10-14T16:28:52.2102565Z [36;1mpython -m pip install --upgrade pip setuptools wheel[0m
2025-10-14T16:28:52.2102877Z [36;1m[0m
2025-10-14T16:28:52.2103103Z [36;1m# Core dependencies with version pinning[0m
2025-10-14T16:28:52.2103479Z [36;1mpip install requests>=2.31.0 pandas>=2.0.0 python-docx>=0.8.11[0m
2025-10-14T16:28:52.2103881Z [36;1mpip install openpyxl>=3.1.0 xlrd>=2.0.1 jinja2>=3.1.0[0m
2025-10-14T16:28:52.2104833Z [36;1mpip install google-auth google-auth-oauthlib google-auth-httplib2[0m
2025-10-14T16:28:52.2105341Z [36;1mpip install google-api-python-client>=2.0.0 PyGithub>=1.55[0m
2025-10-14T16:28:52.2105712Z [36;1mpip install gspread>=5.0.0 oauth2client>=4.1.0[0m
2025-10-14T16:28:52.2106048Z [36;1mpip install beautifulsoup4 lxml urllib3 chardet[0m
2025-10-14T16:28:52.2106370Z [36;1m[0m
2025-10-14T16:28:52.2106555Z [36;1mif [ -f requirements.txt ]; then[0m
2025-10-14T16:28:52.2106835Z [36;1m  pip install -r requirements.txt[0m
2025-10-14T16:28:52.2107153Z [36;1m  echo "Installed requirements from requirements.txt"[0m
2025-10-14T16:28:52.2107445Z [36;1mfi[0m
2025-10-14T16:28:52.2107625Z [36;1m[0m
2025-10-14T16:28:52.2107839Z [36;1mecho "Dependencies installation completed"[0m
2025-10-14T16:28:52.2108113Z [36;1m[0m
2025-10-14T16:28:52.2108345Z [36;1m# Enhanced verification with specific imports[0m
2025-10-14T16:28:52.2108737Z [36;1mpython -c "import pandas, requests; print('Core libraries verified')"[0m
2025-10-14T16:28:52.2109267Z [36;1mpython -c "import docx; print('python-docx verified')" || echo "Warning: python-docx import failed"[0m
2025-10-14T16:28:52.2109938Z [36;1mpython -c "import gspread; print('Google Sheets API verified')" || echo "Warning: Google Sheets API not available"[0m
2025-10-14T16:28:52.2150764Z shell: /usr/bin/bash -e {0}
2025-10-14T16:28:52.2151045Z env:
2025-10-14T16:28:52.2151243Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:28:52.2151534Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:28:52.2151800Z   PYTHON_VERSION: 3.11
2025-10-14T16:28:52.2152021Z   PRODUCTION_MODE: true
2025-10-14T16:28:52.2152233Z   TRACKING_DIR: tracking
2025-10-14T16:28:52.2152476Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:28:52.2152743Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:28:52.2152985Z   CONTACTS_DIR: contacts
2025-10-14T16:28:52.2153195Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:28:52.2153475Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:28:52.2153896Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:28:52.2154508Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:28:52.2154859Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:28:52.2155224Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:28:52.2155579Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:28:52.2155874Z ##[endgroup]
2025-10-14T16:28:52.2229727Z Installing Python dependencies for enhanced production system...
2025-10-14T16:28:54.1350304Z Requirement already satisfied: pip in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (25.2)
2025-10-14T16:28:54.2375250Z Requirement already satisfied: setuptools in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (65.5.0)
2025-10-14T16:28:54.3627244Z Collecting setuptools
2025-10-14T16:28:54.3643317Z   Using cached setuptools-80.9.0-py3-none-any.whl.metadata (6.6 kB)
2025-10-14T16:28:54.3911483Z Collecting wheel
2025-10-14T16:28:54.3926143Z   Using cached wheel-0.45.1-py3-none-any.whl.metadata (2.3 kB)
2025-10-14T16:28:54.4069550Z Using cached setuptools-80.9.0-py3-none-any.whl (1.2 MB)
2025-10-14T16:28:54.4092293Z Using cached wheel-0.45.1-py3-none-any.whl (72 kB)
2025-10-14T16:28:54.4432285Z Installing collected packages: wheel, setuptools
2025-10-14T16:28:54.4898874Z   Attempting uninstall: setuptools
2025-10-14T16:28:54.4914200Z     Found existing installation: setuptools 65.5.0
2025-10-14T16:28:54.8011203Z     Uninstalling setuptools-65.5.0:
2025-10-14T16:28:54.9954322Z       Successfully uninstalled setuptools-65.5.0
2025-10-14T16:28:55.6749821Z 
2025-10-14T16:28:55.6759146Z Successfully installed setuptools-80.9.0 wheel-0.45.1
2025-10-14T16:29:05.3338326Z Collecting google-auth
2025-10-14T16:29:05.3353381Z   Using cached google_auth-2.41.1-py2.py3-none-any.whl.metadata (6.6 kB)
2025-10-14T16:29:05.3536263Z Collecting google-auth-oauthlib
2025-10-14T16:29:05.3550467Z   Using cached google_auth_oauthlib-1.2.2-py3-none-any.whl.metadata (2.7 kB)
2025-10-14T16:29:05.3644906Z Collecting google-auth-httplib2
2025-10-14T16:29:05.3658427Z   Using cached google_auth_httplib2-0.2.0-py2.py3-none-any.whl.metadata (2.2 kB)
2025-10-14T16:29:05.3852441Z Collecting cachetools<7.0,>=2.0.0 (from google-auth)
2025-10-14T16:29:05.4198481Z   Downloading cachetools-6.2.1-py3-none-any.whl.metadata (5.5 kB)
2025-10-14T16:29:05.4384859Z Collecting pyasn1-modules>=0.2.1 (from google-auth)
2025-10-14T16:29:05.4397988Z   Using cached pyasn1_modules-0.4.2-py3-none-any.whl.metadata (3.5 kB)
2025-10-14T16:29:05.4539892Z Collecting rsa<5,>=3.1.4 (from google-auth)
2025-10-14T16:29:05.4553137Z   Using cached rsa-4.9.1-py3-none-any.whl.metadata (5.6 kB)
2025-10-14T16:29:05.4857557Z Collecting pyasn1>=0.1.3 (from rsa<5,>=3.1.4->google-auth)
2025-10-14T16:29:05.4870826Z   Using cached pyasn1-0.6.1-py3-none-any.whl.metadata (8.4 kB)
2025-10-14T16:29:05.5092233Z Collecting requests-oauthlib>=0.7.0 (from google-auth-oauthlib)
2025-10-14T16:29:05.5105445Z   Using cached requests_oauthlib-2.0.0-py2.py3-none-any.whl.metadata (11 kB)
2025-10-14T16:29:05.5234451Z Collecting httplib2>=0.19.0 (from google-auth-httplib2)
2025-10-14T16:29:05.5247389Z   Using cached httplib2-0.31.0-py3-none-any.whl.metadata (2.2 kB)
2025-10-14T16:29:05.5489330Z Collecting pyparsing<4,>=3.0.4 (from httplib2>=0.19.0->google-auth-httplib2)
2025-10-14T16:29:05.5502521Z   Using cached pyparsing-3.2.5-py3-none-any.whl.metadata (5.0 kB)
2025-10-14T16:29:05.5663203Z Collecting oauthlib>=3.0.0 (from requests-oauthlib>=0.7.0->google-auth-oauthlib)
2025-10-14T16:29:05.5676723Z   Using cached oauthlib-3.3.1-py3-none-any.whl.metadata (7.9 kB)
2025-10-14T16:29:05.5700666Z Requirement already satisfied: requests>=2.0.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from requests-oauthlib>=0.7.0->google-auth-oauthlib) (2.32.5)
2025-10-14T16:29:05.5714859Z Requirement already satisfied: charset_normalizer<4,>=2 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from requests>=2.0.0->requests-oauthlib>=0.7.0->google-auth-oauthlib) (3.4.4)
2025-10-14T16:29:05.5719844Z Requirement already satisfied: idna<4,>=2.5 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from requests>=2.0.0->requests-oauthlib>=0.7.0->google-auth-oauthlib) (3.11)
2025-10-14T16:29:05.5725424Z Requirement already satisfied: urllib3<3,>=1.21.1 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from requests>=2.0.0->requests-oauthlib>=0.7.0->google-auth-oauthlib) (2.5.0)
2025-10-14T16:29:05.5730048Z Requirement already satisfied: certifi>=2017.4.17 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from requests>=2.0.0->requests-oauthlib>=0.7.0->google-auth-oauthlib) (2025.10.5)
2025-10-14T16:29:05.5783711Z Using cached google_auth-2.41.1-py2.py3-none-any.whl (221 kB)
2025-10-14T16:29:05.5822438Z Downloading cachetools-6.2.1-py3-none-any.whl (11 kB)
2025-10-14T16:29:05.5857172Z Using cached rsa-4.9.1-py3-none-any.whl (34 kB)
2025-10-14T16:29:05.5870671Z Using cached google_auth_oauthlib-1.2.2-py3-none-any.whl (19 kB)
2025-10-14T16:29:05.5890028Z Using cached google_auth_httplib2-0.2.0-py2.py3-none-any.whl (9.3 kB)
2025-10-14T16:29:05.5902731Z Using cached httplib2-0.31.0-py3-none-any.whl (91 kB)
2025-10-14T16:29:05.5916593Z Using cached pyparsing-3.2.5-py3-none-any.whl (113 kB)
2025-10-14T16:29:05.5929764Z Using cached pyasn1-0.6.1-py3-none-any.whl (83 kB)
2025-10-14T16:29:05.5942662Z Using cached pyasn1_modules-0.4.2-py3-none-any.whl (181 kB)
2025-10-14T16:29:05.5956853Z Using cached requests_oauthlib-2.0.0-py2.py3-none-any.whl (24 kB)
2025-10-14T16:29:05.5969480Z Using cached oauthlib-3.3.1-py3-none-any.whl (160 kB)
2025-10-14T16:29:05.6469573Z Installing collected packages: pyparsing, pyasn1, oauthlib, cachetools, rsa, requests-oauthlib, pyasn1-modules, httplib2, google-auth, google-auth-oauthlib, google-auth-httplib2
2025-10-14T16:29:06.1447963Z 
2025-10-14T16:29:06.1467463Z Successfully installed cachetools-6.2.1 google-auth-2.41.1 google-auth-httplib2-0.2.0 google-auth-oauthlib-1.2.2 httplib2-0.31.0 oauthlib-3.3.1 pyasn1-0.6.1 pyasn1-modules-0.4.2 pyparsing-3.2.5 requests-oauthlib-2.0.0 rsa-4.9.1
2025-10-14T16:29:09.9195027Z Collecting beautifulsoup4
2025-10-14T16:29:09.9209739Z   Using cached beautifulsoup4-4.14.2-py3-none-any.whl.metadata (3.8 kB)
2025-10-14T16:29:09.9232905Z Requirement already satisfied: lxml in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (6.0.2)
2025-10-14T16:29:09.9236932Z Requirement already satisfied: urllib3 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (2.5.0)
2025-10-14T16:29:09.9315199Z Collecting chardet
2025-10-14T16:29:09.9329342Z   Using cached chardet-5.2.0-py3-none-any.whl.metadata (3.4 kB)
2025-10-14T16:29:09.9478113Z Collecting soupsieve>1.2 (from beautifulsoup4)
2025-10-14T16:29:09.9492113Z   Using cached soupsieve-2.8-py3-none-any.whl.metadata (4.6 kB)
2025-10-14T16:29:09.9507226Z Requirement already satisfied: typing-extensions>=4.0.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from beautifulsoup4) (4.15.0)
2025-10-14T16:29:09.9551517Z Using cached beautifulsoup4-4.14.2-py3-none-any.whl (106 kB)
2025-10-14T16:29:09.9565911Z Using cached chardet-5.2.0-py3-none-any.whl (199 kB)
2025-10-14T16:29:09.9580490Z Using cached soupsieve-2.8-py3-none-any.whl (36 kB)
2025-10-14T16:29:10.0141911Z Installing collected packages: soupsieve, chardet, beautifulsoup4
2025-10-14T16:29:10.2897482Z 
2025-10-14T16:29:10.2920882Z Successfully installed beautifulsoup4-4.14.2 chardet-5.2.0 soupsieve-2.8
2025-10-14T16:29:10.6701369Z Requirement already satisfied: gspread in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from -r requirements.txt (line 1)) (6.2.1)
2025-10-14T16:29:10.6705192Z Requirement already satisfied: oauth2client in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from -r requirements.txt (line 2)) (4.1.3)
2025-10-14T16:29:10.6709703Z Requirement already satisfied: PyGithub in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from -r requirements.txt (line 3)) (2.8.1)
2025-10-14T16:29:10.6714888Z Requirement already satisfied: requests>=2.25.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from -r requirements.txt (line 6)) (2.32.5)
2025-10-14T16:29:10.6719432Z Requirement already satisfied: pandas>=1.3.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from -r requirements.txt (line 7)) (2.3.3)
2025-10-14T16:29:10.6724246Z Requirement already satisfied: python-docx>=0.8.11 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from -r requirements.txt (line 8)) (1.2.0)
2025-10-14T16:29:10.6728810Z Requirement already satisfied: openpyxl>=3.0.9 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from -r requirements.txt (line 9)) (3.1.5)
2025-10-14T16:29:10.6734531Z Requirement already satisfied: google-auth>=2.0.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from -r requirements.txt (line 13)) (2.41.1)
2025-10-14T16:29:10.6738913Z Requirement already satisfied: google-auth-oauthlib>=0.5.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from -r requirements.txt (line 14)) (1.2.2)
2025-10-14T16:29:10.6743719Z Requirement already satisfied: google-auth-httplib2>=0.1.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from -r requirements.txt (line 15)) (0.2.0)
2025-10-14T16:29:10.6748148Z Requirement already satisfied: google-api-python-client>=2.0.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from -r requirements.txt (line 16)) (2.184.0)
2025-10-14T16:29:10.7201011Z Collecting email-validator>=1.1.0 (from -r requirements.txt (line 19))
2025-10-14T16:29:10.7215970Z   Using cached email_validator-2.3.0-py3-none-any.whl.metadata (26 kB)
2025-10-14T16:29:10.7546293Z Collecting pytest>=6.0.0 (from -r requirements.txt (line 22))
2025-10-14T16:29:10.7560587Z   Using cached pytest-8.4.2-py3-none-any.whl.metadata (7.7 kB)
2025-10-14T16:29:10.7706174Z Collecting pytest-cov>=2.10.0 (from -r requirements.txt (line 23))
2025-10-14T16:29:10.7720296Z   Using cached pytest_cov-7.0.0-py3-none-any.whl.metadata (31 kB)
2025-10-14T16:29:10.8254628Z Collecting black>=21.0.0 (from -r requirements.txt (line 24))
2025-10-14T16:29:10.8270092Z   Using cached black-25.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl.metadata (83 kB)
2025-10-14T16:29:10.8507990Z Collecting flake8>=3.8.0 (from -r requirements.txt (line 25))
2025-10-14T16:29:10.8521757Z   Using cached flake8-7.3.0-py2.py3-none-any.whl.metadata (3.8 kB)
2025-10-14T16:29:10.8869637Z Collecting pyyaml (from -r requirements.txt (line 27))
2025-10-14T16:29:10.8884285Z   Using cached pyyaml-6.0.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.4 kB)
2025-10-14T16:29:10.8913750Z Requirement already satisfied: httplib2>=0.9.1 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from oauth2client->-r requirements.txt (line 2)) (0.31.0)
2025-10-14T16:29:10.8919868Z Requirement already satisfied: pyasn1>=0.1.7 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from oauth2client->-r requirements.txt (line 2)) (0.6.1)
2025-10-14T16:29:10.8926087Z Requirement already satisfied: pyasn1-modules>=0.0.5 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from oauth2client->-r requirements.txt (line 2)) (0.4.2)
2025-10-14T16:29:10.8931789Z Requirement already satisfied: rsa>=3.1.4 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from oauth2client->-r requirements.txt (line 2)) (4.9.1)
2025-10-14T16:29:10.8937655Z Requirement already satisfied: six>=1.6.1 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from oauth2client->-r requirements.txt (line 2)) (1.17.0)
2025-10-14T16:29:10.8947396Z Requirement already satisfied: pynacl>=1.4.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from PyGithub->-r requirements.txt (line 3)) (1.6.0)
2025-10-14T16:29:10.8958199Z Requirement already satisfied: pyjwt>=2.4.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from pyjwt[crypto]>=2.4.0->PyGithub->-r requirements.txt (line 3)) (2.10.1)
2025-10-14T16:29:10.8965289Z Requirement already satisfied: typing-extensions>=4.5.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from PyGithub->-r requirements.txt (line 3)) (4.15.0)
2025-10-14T16:29:10.8970411Z Requirement already satisfied: urllib3>=1.26.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from PyGithub->-r requirements.txt (line 3)) (2.5.0)
2025-10-14T16:29:10.8981941Z Requirement already satisfied: charset_normalizer<4,>=2 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from requests>=2.25.0->-r requirements.txt (line 6)) (3.4.4)
2025-10-14T16:29:10.8987620Z Requirement already satisfied: idna<4,>=2.5 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from requests>=2.25.0->-r requirements.txt (line 6)) (3.11)
2025-10-14T16:29:10.8995221Z Requirement already satisfied: certifi>=2017.4.17 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from requests>=2.25.0->-r requirements.txt (line 6)) (2025.10.5)
2025-10-14T16:29:10.9090535Z Requirement already satisfied: numpy>=1.23.2 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from pandas>=1.3.0->-r requirements.txt (line 7)) (2.3.3)
2025-10-14T16:29:10.9097359Z Requirement already satisfied: python-dateutil>=2.8.2 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from pandas>=1.3.0->-r requirements.txt (line 7)) (2.9.0.post0)
2025-10-14T16:29:10.9102930Z Requirement already satisfied: pytz>=2020.1 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from pandas>=1.3.0->-r requirements.txt (line 7)) (2025.2)
2025-10-14T16:29:10.9108180Z Requirement already satisfied: tzdata>=2022.7 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from pandas>=1.3.0->-r requirements.txt (line 7)) (2025.2)
2025-10-14T16:29:10.9197926Z Requirement already satisfied: lxml>=3.1.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from python-docx>=0.8.11->-r requirements.txt (line 8)) (6.0.2)
2025-10-14T16:29:10.9210367Z Requirement already satisfied: et-xmlfile in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from openpyxl>=3.0.9->-r requirements.txt (line 9)) (2.0.0)
2025-10-14T16:29:10.9224692Z Requirement already satisfied: cachetools<7.0,>=2.0.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from google-auth>=2.0.0->-r requirements.txt (line 13)) (6.2.1)
2025-10-14T16:29:10.9290821Z Requirement already satisfied: requests-oauthlib>=0.7.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from google-auth-oauthlib>=0.5.0->-r requirements.txt (line 14)) (2.0.0)
2025-10-14T16:29:10.9326208Z Requirement already satisfied: google-api-core!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0,>=1.31.5 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from google-api-python-client>=2.0.0->-r requirements.txt (line 16)) (2.26.0)
2025-10-14T16:29:10.9332158Z Requirement already satisfied: uritemplate<5,>=3.0.1 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from google-api-python-client>=2.0.0->-r requirements.txt (line 16)) (4.2.0)
2025-10-14T16:29:10.9347774Z Requirement already satisfied: googleapis-common-protos<2.0.0,>=1.56.2 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from google-api-core!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0,>=1.31.5->google-api-python-client>=2.0.0->-r requirements.txt (line 16)) (1.70.0)
2025-10-14T16:29:10.9357499Z Requirement already satisfied: protobuf!=3.20.0,!=3.20.1,!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5,<7.0.0,>=3.19.5 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from google-api-core!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0,>=1.31.5->google-api-python-client>=2.0.0->-r requirements.txt (line 16)) (6.32.1)
2025-10-14T16:29:10.9363272Z Requirement already satisfied: proto-plus<2.0.0,>=1.22.3 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from google-api-core!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0,<3.0.0,>=1.31.5->google-api-python-client>=2.0.0->-r requirements.txt (line 16)) (1.26.1)
2025-10-14T16:29:10.9417374Z Requirement already satisfied: pyparsing<4,>=3.0.4 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from httplib2>=0.9.1->oauth2client->-r requirements.txt (line 2)) (3.2.5)
2025-10-14T16:29:10.9569055Z Collecting dnspython>=2.0.0 (from email-validator>=1.1.0->-r requirements.txt (line 19))
2025-10-14T16:29:10.9582819Z   Using cached dnspython-2.8.0-py3-none-any.whl.metadata (5.7 kB)
2025-10-14T16:29:10.9700352Z Collecting iniconfig>=1 (from pytest>=6.0.0->-r requirements.txt (line 22))
2025-10-14T16:29:10.9714297Z   Using cached iniconfig-2.1.0-py3-none-any.whl.metadata (2.7 kB)
2025-10-14T16:29:10.9851476Z Collecting packaging>=20 (from pytest>=6.0.0->-r requirements.txt (line 22))
2025-10-14T16:29:10.9864813Z   Using cached packaging-25.0-py3-none-any.whl.metadata (3.3 kB)
2025-10-14T16:29:10.9965597Z Collecting pluggy<2,>=1.5 (from pytest>=6.0.0->-r requirements.txt (line 22))
2025-10-14T16:29:10.9978960Z   Using cached pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
2025-10-14T16:29:11.0195631Z Collecting pygments>=2.7.2 (from pytest>=6.0.0->-r requirements.txt (line 22))
2025-10-14T16:29:11.0208963Z   Using cached pygments-2.19.2-py3-none-any.whl.metadata (2.5 kB)
2025-10-14T16:29:11.3315812Z Collecting coverage>=7.10.6 (from coverage[toml]>=7.10.6->pytest-cov>=2.10.0->-r requirements.txt (line 23))
2025-10-14T16:29:11.3330951Z   Using cached coverage-7.10.7-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (8.9 kB)
2025-10-14T16:29:11.3615111Z Collecting click>=8.0.0 (from black>=21.0.0->-r requirements.txt (line 24))
2025-10-14T16:29:11.3628772Z   Using cached click-8.3.0-py3-none-any.whl.metadata (2.6 kB)
2025-10-14T16:29:11.3704978Z Collecting mypy-extensions>=0.4.3 (from black>=21.0.0->-r requirements.txt (line 24))
2025-10-14T16:29:11.3718533Z   Using cached mypy_extensions-1.1.0-py3-none-any.whl.metadata (1.1 kB)
2025-10-14T16:29:11.3843461Z Collecting pathspec>=0.9.0 (from black>=21.0.0->-r requirements.txt (line 24))
2025-10-14T16:29:11.3856954Z   Using cached pathspec-0.12.1-py3-none-any.whl.metadata (21 kB)
2025-10-14T16:29:11.4029524Z Collecting platformdirs>=2 (from black>=21.0.0->-r requirements.txt (line 24))
2025-10-14T16:29:11.4341269Z   Downloading platformdirs-4.5.0-py3-none-any.whl.metadata (12 kB)
2025-10-14T16:29:11.4453775Z Collecting pytokens>=0.1.10 (from black>=21.0.0->-r requirements.txt (line 24))
2025-10-14T16:29:11.4467259Z   Using cached pytokens-0.1.10-py3-none-any.whl.metadata (2.0 kB)
2025-10-14T16:29:11.4582706Z Collecting mccabe<0.8.0,>=0.7.0 (from flake8>=3.8.0->-r requirements.txt (line 25))
2025-10-14T16:29:11.4596331Z   Using cached mccabe-0.7.0-py2.py3-none-any.whl.metadata (5.0 kB)
2025-10-14T16:29:11.4689589Z Collecting pycodestyle<2.15.0,>=2.14.0 (from flake8>=3.8.0->-r requirements.txt (line 25))
2025-10-14T16:29:11.4703155Z   Using cached pycodestyle-2.14.0-py2.py3-none-any.whl.metadata (4.5 kB)
2025-10-14T16:29:11.4825700Z Collecting pyflakes<3.5.0,>=3.4.0 (from flake8>=3.8.0->-r requirements.txt (line 25))
2025-10-14T16:29:11.4839120Z   Using cached pyflakes-3.4.0-py2.py3-none-any.whl.metadata (3.5 kB)
2025-10-14T16:29:11.5104866Z Requirement already satisfied: cryptography>=3.4.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from pyjwt[crypto]>=2.4.0->PyGithub->-r requirements.txt (line 3)) (46.0.2)
2025-10-14T16:29:11.5128050Z Requirement already satisfied: cffi>=2.0.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from cryptography>=3.4.0->pyjwt[crypto]>=2.4.0->PyGithub->-r requirements.txt (line 3)) (2.0.0)
2025-10-14T16:29:11.5165606Z Requirement already satisfied: pycparser in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from cffi>=2.0.0->cryptography>=3.4.0->pyjwt[crypto]>=2.4.0->PyGithub->-r requirements.txt (line 3)) (2.23)
2025-10-14T16:29:11.5240563Z Requirement already satisfied: oauthlib>=3.0.0 in /opt/hostedtoolcache/Python/3.11.13/x64/lib/python3.11/site-packages (from requests-oauthlib>=0.7.0->google-auth-oauthlib>=0.5.0->-r requirements.txt (line 14)) (3.3.1)
2025-10-14T16:29:11.5338506Z Using cached email_validator-2.3.0-py3-none-any.whl (35 kB)
2025-10-14T16:29:11.5352014Z Using cached pytest-8.4.2-py3-none-any.whl (365 kB)
2025-10-14T16:29:11.5367674Z Using cached pluggy-1.6.0-py3-none-any.whl (20 kB)
2025-10-14T16:29:11.5380919Z Using cached pytest_cov-7.0.0-py3-none-any.whl (22 kB)
2025-10-14T16:29:11.5394608Z Using cached black-25.9.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl (1.6 MB)
2025-10-14T16:29:11.5419128Z Using cached flake8-7.3.0-py2.py3-none-any.whl (57 kB)
2025-10-14T16:29:11.5432465Z Using cached mccabe-0.7.0-py2.py3-none-any.whl (7.3 kB)
2025-10-14T16:29:11.5445612Z Using cached pycodestyle-2.14.0-py2.py3-none-any.whl (31 kB)
2025-10-14T16:29:11.5459009Z Using cached pyflakes-3.4.0-py2.py3-none-any.whl (63 kB)
2025-10-14T16:29:11.5472787Z Using cached pyyaml-6.0.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (806 kB)
2025-10-14T16:29:11.5493796Z Using cached click-8.3.0-py3-none-any.whl (107 kB)
2025-10-14T16:29:11.5508452Z Using cached coverage-7.10.7-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (250 kB)
2025-10-14T16:29:11.5522953Z Using cached dnspython-2.8.0-py3-none-any.whl (331 kB)
2025-10-14T16:29:11.5538545Z Using cached iniconfig-2.1.0-py3-none-any.whl (6.0 kB)
2025-10-14T16:29:11.5551921Z Using cached mypy_extensions-1.1.0-py3-none-any.whl (5.0 kB)
2025-10-14T16:29:11.5565125Z Using cached packaging-25.0-py3-none-any.whl (66 kB)
2025-10-14T16:29:11.5578226Z Using cached pathspec-0.12.1-py3-none-any.whl (31 kB)
2025-10-14T16:29:11.5613927Z Downloading platformdirs-4.5.0-py3-none-any.whl (18 kB)
2025-10-14T16:29:11.5661290Z Using cached pygments-2.19.2-py3-none-any.whl (1.2 MB)
2025-10-14T16:29:11.5682888Z Using cached pytokens-0.1.10-py3-none-any.whl (12 kB)
2025-10-14T16:29:11.6444962Z Installing collected packages: pyyaml, pytokens, pygments, pyflakes, pycodestyle, pluggy, platformdirs, pathspec, packaging, mypy-extensions, mccabe, iniconfig, dnspython, coverage, click, pytest, flake8, email-validator, black, pytest-cov
2025-10-14T16:29:13.2018281Z 
2025-10-14T16:29:13.2050983Z Successfully installed black-25.9.0 click-8.3.0 coverage-7.10.7 dnspython-2.8.0 email-validator-2.3.0 flake8-7.3.0 iniconfig-2.1.0 mccabe-0.7.0 mypy-extensions-1.1.0 packaging-25.0 pathspec-0.12.1 platformdirs-4.5.0 pluggy-1.6.0 pycodestyle-2.14.0 pyflakes-3.4.0 pygments-2.19.2 pytest-8.4.2 pytest-cov-7.0.0 pytokens-0.1.10 pyyaml-6.0.3
2025-10-14T16:29:13.2876484Z Installed requirements from requirements.txt
2025-10-14T16:29:13.2877144Z Dependencies installation completed
2025-10-14T16:29:13.8500726Z Core libraries verified
2025-10-14T16:29:13.9706830Z python-docx verified
2025-10-14T16:29:14.5751729Z Google Sheets API verified
2025-10-14T16:29:14.6032622Z ##[group]Run echo "Creating enhanced directory structure..."
2025-10-14T16:29:14.6033073Z [36;1mecho "Creating enhanced directory structure..."[0m
2025-10-14T16:29:14.6033358Z [36;1m[0m
2025-10-14T16:29:14.6033612Z [36;1m# Use absolute paths to avoid any path resolution issues[0m
2025-10-14T16:29:14.6033923Z [36;1mWORK_DIR="$PWD"[0m
2025-10-14T16:29:14.6034328Z [36;1m[0m
2025-10-14T16:29:14.6034538Z [36;1m# Create all directories with absolute paths[0m
2025-10-14T16:29:14.6034841Z [36;1mmkdir -p "$WORK_DIR/$TEMPLATES_DIR"[0m
2025-10-14T16:29:14.6035113Z [36;1mmkdir -p "$WORK_DIR/$CONTACTS_DIR" [0m
2025-10-14T16:29:14.6035383Z [36;1mmkdir -p "$WORK_DIR/$SCHEDULED_DIR"[0m
2025-10-14T16:29:14.6035648Z [36;1mmkdir -p "$WORK_DIR/$TRACKING_DIR"[0m
2025-10-14T16:29:14.6035900Z [36;1mmkdir -p "$WORK_DIR/utils"[0m
2025-10-14T16:29:14.6036137Z [36;1mmkdir -p "$WORK_DIR/reports"[0m
2025-10-14T16:29:14.6036365Z [36;1m[0m
2025-10-14T16:29:14.6036630Z [36;1m# Create comprehensive tracking subdirectories[0m
2025-10-14T16:29:14.6037143Z [36;1mmkdir -p "$WORK_DIR/$TRACKING_DIR"/{feedback_responses,domain_stats,execution_logs,batch_reports,reply_tracking}[0m
2025-10-14T16:29:14.6037819Z [36;1mmkdir -p "$WORK_DIR/$TEMPLATES_DIR"/{education,finance,healthcare,industry,technology,government}[0m
2025-10-14T16:29:14.6038325Z [36;1mmkdir -p "$WORK_DIR/$CONTACTS_DIR"/{csv,excel,docx,urls}[0m
2025-10-14T16:29:14.6038612Z [36;1m[0m
2025-10-14T16:29:14.6038818Z [36;1mecho "Enhanced directory structure created:"[0m
2025-10-14T16:29:14.6039107Z [36;1mecho "  Working directory: $WORK_DIR"[0m
2025-10-14T16:29:14.6039397Z [36;1mecho "  Templates: $WORK_DIR/$TEMPLATES_DIR"[0m
2025-10-14T16:29:14.6039690Z [36;1mecho "  Contacts: $WORK_DIR/$CONTACTS_DIR"[0m
2025-10-14T16:29:14.6039980Z [36;1mecho "  Scheduled: $WORK_DIR/$SCHEDULED_DIR"[0m
2025-10-14T16:29:14.6040265Z [36;1mecho "  Tracking: $WORK_DIR/$TRACKING_DIR"[0m
2025-10-14T16:29:14.6040510Z [36;1m[0m
2025-10-14T16:29:14.6040731Z [36;1m# Verify directories exist with detailed checking[0m
2025-10-14T16:29:14.6041188Z [36;1mfor dir in "$TEMPLATES_DIR" "$CONTACTS_DIR" "$SCHEDULED_DIR" "$TRACKING_DIR" "utils" "reports"; do[0m
2025-10-14T16:29:14.6041607Z [36;1m  if [ -d "$WORK_DIR/$dir" ]; then[0m
2025-10-14T16:29:14.6041899Z [36;1m    echo "✅ $dir directory created successfully"[0m
2025-10-14T16:29:14.6042167Z [36;1m  else[0m
2025-10-14T16:29:14.6042383Z [36;1m    echo "❌ Failed to create $dir directory"[0m
2025-10-14T16:29:14.6042634Z [36;1m    exit 1[0m
2025-10-14T16:29:14.6042814Z [36;1m  fi[0m
2025-10-14T16:29:14.6042977Z [36;1mdone[0m
2025-10-14T16:29:14.6075520Z shell: /usr/bin/bash -e {0}
2025-10-14T16:29:14.6075741Z env:
2025-10-14T16:29:14.6075926Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:14.6076204Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:14.6076459Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:14.6076662Z   PRODUCTION_MODE: true
2025-10-14T16:29:14.6076876Z   TRACKING_DIR: tracking
2025-10-14T16:29:14.6077088Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:14.6077336Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:14.6077569Z   CONTACTS_DIR: contacts
2025-10-14T16:29:14.6077772Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:14.6078045Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6078433Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:14.6078808Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6079149Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6079493Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6079834Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:14.6080120Z ##[endgroup]
2025-10-14T16:29:14.6130941Z Creating enhanced directory structure...
2025-10-14T16:29:14.6239369Z Enhanced directory structure created:
2025-10-14T16:29:14.6240521Z   Working directory: /home/runner/work/email-campaign-manager/email-campaign-manager
2025-10-14T16:29:14.6241511Z   Templates: /home/runner/work/email-campaign-manager/email-campaign-manager/campaign-templates
2025-10-14T16:29:14.6242296Z   Contacts: /home/runner/work/email-campaign-manager/email-campaign-manager/contacts
2025-10-14T16:29:14.6243144Z   Scheduled: /home/runner/work/email-campaign-manager/email-campaign-manager/scheduled-campaigns
2025-10-14T16:29:14.6244848Z   Tracking: /home/runner/work/email-campaign-manager/email-campaign-manager/tracking
2025-10-14T16:29:14.6245869Z ✅ campaign-templates directory created successfully
2025-10-14T16:29:14.6246408Z ✅ contacts directory created successfully
2025-10-14T16:29:14.6246756Z ✅ scheduled-campaigns directory created successfully
2025-10-14T16:29:14.6247096Z ✅ tracking directory created successfully
2025-10-14T16:29:14.6247468Z ✅ utils directory created successfully
2025-10-14T16:29:14.6247788Z ✅ reports directory created successfully
2025-10-14T16:29:14.6267133Z ##[group]Run echo "Ensuring test data exists before validation..."
2025-10-14T16:29:14.6267589Z [36;1mecho "Ensuring test data exists before validation..."[0m
2025-10-14T16:29:14.6267925Z [36;1mCONTACTS_PATH="$PWD/$CONTACTS_DIR"[0m
2025-10-14T16:29:14.6268207Z [36;1mSCHEDULED_PATH="$PWD/$SCHEDULED_DIR"[0m
2025-10-14T16:29:14.6268457Z [36;1m[0m
2025-10-14T16:29:14.6268669Z [36;1m# Always create test data if it doesn't exist[0m
2025-10-14T16:29:14.6269013Z [36;1mif [ ! -f "$CONTACTS_PATH/enhanced_test_contacts.csv" ]; then[0m
2025-10-14T16:29:14.6269385Z [36;1m  cat > "$CONTACTS_PATH/enhanced_test_contacts.csv" << 'EOF'[0m
2025-10-14T16:29:14.6269740Z [36;1mname,email,organization,role,domain,country[0m
2025-10-14T16:29:14.6270130Z [36;1mJohn Doe,john.doe@example.com,Example Corp,Manager,education,US[0m
2025-10-14T16:29:14.6270582Z [36;1mJane Smith,jane.smith@test.org,Test Organization,Director,healthcare,UK[0m
2025-10-14T16:29:14.6271093Z [36;1mBob Johnson,bob.johnson@sample.net,Sample Company,Analyst,finance,CA[0m
2025-10-14T16:29:14.6271566Z [36;1mAlice Brown,alice.brown@demo.edu,Demo University,Professor,education,US[0m
2025-10-14T16:29:14.6272045Z [36;1mCharlie Wilson,charlie.wilson@tech.co,Tech Solutions,CTO,technology,DE[0m
2025-10-14T16:29:14.6272394Z [36;1mEOF[0m
2025-10-14T16:29:14.6272599Z [36;1m  echo "✅ Test contact data created"[0m
2025-10-14T16:29:14.6272848Z [36;1mfi[0m
2025-10-14T16:29:14.6273005Z [36;1m[0m
2025-10-14T16:29:14.6273194Z [36;1m# Verify file exists and has content[0m
2025-10-14T16:29:14.6273509Z [36;1mif [ -f "$CONTACTS_PATH/enhanced_test_contacts.csv" ]; then[0m
2025-10-14T16:29:14.6274084Z [36;1m  echo "Contact file exists with $(wc -l < "$CONTACTS_PATH/enhanced_test_contacts.csv") lines"[0m
2025-10-14T16:29:14.6274528Z [36;1m  head -5 "$CONTACTS_PATH/enhanced_test_contacts.csv"[0m
2025-10-14T16:29:14.6274799Z [36;1mfi[0m
2025-10-14T16:29:14.6274962Z [36;1m[0m
2025-10-14T16:29:14.6275149Z [36;1m# Create test campaign[0m
2025-10-14T16:29:14.6275457Z [36;1mif [ ! -f "$SCHEDULED_PATH/enhanced_welcome_campaign.txt" ]; then[0m
2025-10-14T16:29:14.6275849Z [36;1m  cat > "$SCHEDULED_PATH/enhanced_welcome_campaign.txt" << 'EOF'[0m
2025-10-14T16:29:14.6276248Z [36;1mSubject: Welcome {{name}} from {{organization}} to Our Platform![0m
2025-10-14T16:29:14.6276558Z [36;1m[0m
2025-10-14T16:29:14.6276722Z [36;1mDear {{name}},[0m
2025-10-14T16:29:14.6276917Z [36;1m[0m
2025-10-14T16:29:14.6277183Z [36;1mWe're excited to welcome you! This message is being sent to {{email}}.[0m
2025-10-14T16:29:14.6277496Z [36;1m[0m
2025-10-14T16:29:14.6277752Z [36;1mYour organization, {{organization}}, in the {{domain}} sector.[0m
2025-10-14T16:29:14.6278060Z [36;1m[0m
2025-10-14T16:29:14.6278223Z [36;1mBest regards,[0m
2025-10-14T16:29:14.6278426Z [36;1mThe Platform Team[0m
2025-10-14T16:29:14.6278629Z [36;1mEOF[0m
2025-10-14T16:29:14.6278839Z [36;1m  echo "✅ Test campaign template created"[0m
2025-10-14T16:29:14.6279257Z [36;1mfi[0m
2025-10-14T16:29:14.6279417Z [36;1m[0m
2025-10-14T16:29:14.6279582Z [36;1m# Verify creation[0m
2025-10-14T16:29:14.6279799Z [36;1mecho "Verification:"[0m
2025-10-14T16:29:14.6280027Z [36;1mls -lh "$CONTACTS_PATH/"[0m
2025-10-14T16:29:14.6280437Z [36;1mecho "Test file lines: $(wc -l < "$CONTACTS_PATH/enhanced_test_contacts.csv" 2>/dev/null || echo 0)"[0m
2025-10-14T16:29:14.6310301Z shell: /usr/bin/bash -e {0}
2025-10-14T16:29:14.6310521Z env:
2025-10-14T16:29:14.6310709Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:14.6310981Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:14.6311239Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:14.6311442Z   PRODUCTION_MODE: true
2025-10-14T16:29:14.6311640Z   TRACKING_DIR: tracking
2025-10-14T16:29:14.6311852Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:14.6312099Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:14.6312333Z   CONTACTS_DIR: contacts
2025-10-14T16:29:14.6312550Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:14.6313006Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6313412Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:14.6313790Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6314249Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6314595Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6314934Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:14.6315221Z ##[endgroup]
2025-10-14T16:29:14.6362897Z Ensuring test data exists before validation...
2025-10-14T16:29:14.6375215Z ✅ Test contact data created
2025-10-14T16:29:14.6396303Z Contact file exists with 6 lines
2025-10-14T16:29:14.6409844Z name,email,organization,role,domain,country
2025-10-14T16:29:14.6410305Z John Doe,john.doe@example.com,Example Corp,Manager,education,US
2025-10-14T16:29:14.6410958Z Jane Smith,jane.smith@test.org,Test Organization,Director,healthcare,UK
2025-10-14T16:29:14.6411879Z Bob Johnson,bob.johnson@sample.net,Sample Company,Analyst,finance,CA
2025-10-14T16:29:14.6412757Z Alice Brown,alice.brown@demo.edu,Demo University,Professor,education,US
2025-10-14T16:29:14.6423268Z ✅ Test campaign template created
2025-10-14T16:29:14.6423717Z Verification:
2025-10-14T16:29:14.6436843Z total 32K
2025-10-14T16:29:14.6437407Z -rw-r--r-- 1 runner runner  244 Oct 14 16:28 banks_contacts_20250925_184246.csv
2025-10-14T16:29:14.6438170Z drwxr-xr-x 2 runner runner 4.0K Oct 14 16:29 csv
2025-10-14T16:29:14.6438825Z drwxr-xr-x 2 runner runner 4.0K Oct 14 16:29 docx
2025-10-14T16:29:14.6439603Z -rw-r--r-- 1 runner runner  887 Oct 14 16:28 edu_adults_contacts_20251004_121252.csv
2025-10-14T16:29:14.6440467Z -rw-r--r-- 1 runner runner  392 Oct 14 16:29 enhanced_test_contacts.csv
2025-10-14T16:29:14.6440924Z drwxr-xr-x 2 runner runner 4.0K Oct 14 16:29 excel
2025-10-14T16:29:14.6441337Z -rw-r--r-- 1 runner runner    0 Oct 14 16:28 reply_log.jsonl
2025-10-14T16:29:14.6441818Z -rw-r--r-- 1 runner runner   85 Oct 14 16:28 suppression_list.json
2025-10-14T16:29:14.6442281Z -rw-r--r-- 1 runner runner    0 Oct 14 16:28 suppression_log.jsonl
2025-10-14T16:29:14.6442726Z drwxr-xr-x 2 runner runner 4.0K Oct 14 16:29 urls
2025-10-14T16:29:14.6454406Z Test file lines: 6
2025-10-14T16:29:14.6671526Z ##[group]Run echo "$GOOGLE_SVC_JSON" | base64 -d > /tmp/google_svc.json
2025-10-14T16:29:14.6671992Z [36;1mecho "$GOOGLE_SVC_JSON" | base64 -d > /tmp/google_svc.json[0m
2025-10-14T16:29:14.6672322Z [36;1mchmod 600 /tmp/google_svc.json[0m
2025-10-14T16:29:14.6672696Z [36;1mecho "GOOGLE_APPLICATION_CREDENTIALS=/tmp/google_svc.json" >> $GITHUB_ENV[0m
2025-10-14T16:29:14.6673102Z [36;1mecho "✅ Google credentials configured"[0m
2025-10-14T16:29:14.6702163Z shell: /usr/bin/bash -e {0}
2025-10-14T16:29:14.6702389Z env:
2025-10-14T16:29:14.6702578Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:14.6702849Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:14.6703248Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:14.6703444Z   PRODUCTION_MODE: true
2025-10-14T16:29:14.6703644Z   TRACKING_DIR: tracking
2025-10-14T16:29:14.6703862Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:14.6704414Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:14.6704805Z   CONTACTS_DIR: contacts
2025-10-14T16:29:14.6705122Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:14.6705573Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6706163Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:14.6706551Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6706897Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6707247Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6707586Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:14.6800361Z   GOOGLE_SVC_JSON: ***
2025-10-14T16:29:14.6800580Z ##[endgroup]
2025-10-14T16:29:14.6879550Z ✅ Google credentials configured
2025-10-14T16:29:14.6900464Z ##[group]Run echo "Running comprehensive system validation..."
2025-10-14T16:29:14.6900938Z [36;1mecho "Running comprehensive system validation..."[0m
2025-10-14T16:29:14.6901228Z [36;1m[0m
2025-10-14T16:29:14.6901404Z [36;1moverall_status=0[0m
2025-10-14T16:29:14.6901706Z [36;1mvalidation_report="# Enhanced System Validation Report\n\n"[0m
2025-10-14T16:29:14.6902011Z [36;1m[0m
2025-10-14T16:29:14.6902411Z [36;1m# Check if main scripts exist and can import[0m
2025-10-14T16:29:14.6920354Z [36;1mecho "Checking for campaign system scripts..."[0m
2025-10-14T16:29:14.6920665Z [36;1m[0m
2025-10-14T16:29:14.6920885Z [36;1m# Enhanced docx_parser.py validation[0m
2025-10-14T16:29:14.6921194Z [36;1mif [ -f "utils/docx_parser.py" ]; then[0m
2025-10-14T16:29:14.6921498Z [36;1m  echo "✅ Found utils/docx_parser.py"[0m
2025-10-14T16:29:14.6921757Z [36;1m  [0m
2025-10-14T16:29:14.6921952Z [36;1m  python << 'EOF'[0m
2025-10-14T16:29:14.6922178Z [36;1mimport sys[0m
2025-10-14T16:29:14.6922420Z [36;1msys.path.append('.')[0m
2025-10-14T16:29:14.6922677Z [36;1msys.path.append('utils')[0m
2025-10-14T16:29:14.6922903Z [36;1mtry:[0m
2025-10-14T16:29:14.6923174Z [36;1m  # Test if docx_parser can be imported and has expected functions[0m
2025-10-14T16:29:14.6923532Z [36;1m  import utils.docx_parser as parser[0m
2025-10-14T16:29:14.6923870Z [36;1m  print('✅ utils/docx_parser.py imports successfully')[0m
2025-10-14T16:29:14.6924387Z [36;1m  [0m
2025-10-14T16:29:14.6924597Z [36;1m  # Check for main execution capability[0m
2025-10-14T16:29:14.6924931Z [36;1m  if hasattr(parser, 'main') or hasattr(parser, '__main__'):[0m
2025-10-14T16:29:14.6925291Z [36;1m    print('  - Main execution function available')[0m
2025-10-14T16:29:14.6925563Z [36;1m  else:[0m
2025-10-14T16:29:14.6925788Z [36;1m    print('  - Script is executable as module')[0m
2025-10-14T16:29:14.6926070Z [36;1mexcept Exception as e:[0m
2025-10-14T16:29:14.6926347Z [36;1m  print(f'❌ docx_parser.py import error: {e}')[0m
2025-10-14T16:29:14.6926620Z [36;1m  sys.exit(1)[0m
2025-10-14T16:29:14.6926817Z [36;1mEOF[0m
2025-10-14T16:29:14.6926982Z [36;1m  [0m
2025-10-14T16:29:14.6927154Z [36;1m  if [ $? -eq 0 ]; then[0m
2025-10-14T16:29:14.6927460Z [36;1m    validation_report+="## Main Campaign Processor: PASSED\n"[0m
2025-10-14T16:29:14.6927767Z [36;1m  else[0m
2025-10-14T16:29:14.6927952Z [36;1m    overall_status=1[0m
2025-10-14T16:29:14.6928237Z [36;1m    validation_report+="## Main Campaign Processor: FAILED\n"[0m
2025-10-14T16:29:14.6928571Z [36;1m    echo "❌ docx_parser.py import failed"[0m
2025-10-14T16:29:14.6928821Z [36;1m  fi[0m
2025-10-14T16:29:14.6928989Z [36;1melse[0m
2025-10-14T16:29:14.6929201Z [36;1m  echo "❌ utils/docx_parser.py not found"[0m
2025-10-14T16:29:14.6929458Z [36;1m  overall_status=1[0m
2025-10-14T16:29:14.6929795Z [36;1m  validation_report+="## Main Campaign Processor: FAILED - File not found\n"[0m
2025-10-14T16:29:14.6930356Z [36;1mfi[0m
2025-10-14T16:29:14.6930532Z [36;1m[0m
2025-10-14T16:29:14.6930721Z [36;1m# Check feedback system scripts[0m
2025-10-14T16:29:14.6931215Z [36;1mfeedback_scripts=("utils/email_feedback_injector.py" "utils/docx_feedback_processor.py" "utils/reply_tracker.py")[0m
2025-10-14T16:29:14.6931704Z [36;1mfeedback_available=0[0m
2025-10-14T16:29:14.6931912Z [36;1m[0m
2025-10-14T16:29:14.6932128Z [36;1mfor script in "${feedback_scripts[@]}"; do[0m
2025-10-14T16:29:14.6932408Z [36;1m  if [ -f "$script" ]; then[0m
2025-10-14T16:29:14.6932646Z [36;1m    echo "✅ Found $script"[0m
2025-10-14T16:29:14.6932927Z [36;1m    feedback_available=$((feedback_available + 1))[0m
2025-10-14T16:29:14.6933204Z [36;1m    [0m
2025-10-14T16:29:14.6933405Z [36;1m    # Extract module name from path[0m
2025-10-14T16:29:14.6933678Z [36;1m    module_name=$(basename "$script" .py)[0m
2025-10-14T16:29:14.6933930Z [36;1m    [0m
2025-10-14T16:29:14.6934322Z [36;1m    python << EOF[0m
2025-10-14T16:29:14.6934536Z [36;1mimport sys[0m
2025-10-14T16:29:14.6934906Z [36;1msys.path.append('.')[0m
2025-10-14T16:29:14.6935143Z [36;1msys.path.append('utils')[0m
2025-10-14T16:29:14.6935365Z [36;1mtry:[0m
2025-10-14T16:29:14.6935550Z [36;1m  __import__('$module_name')[0m
2025-10-14T16:29:14.6935828Z [36;1m  print('✅ $module_name imports successfully')[0m
2025-10-14T16:29:14.6936104Z [36;1mexcept Exception as e:[0m
2025-10-14T16:29:14.6936365Z [36;1m  print('⚠️ $module_name import warning:', e)[0m
2025-10-14T16:29:14.6936622Z [36;1mEOF[0m
2025-10-14T16:29:14.6936791Z [36;1m  else[0m
2025-10-14T16:29:14.6936978Z [36;1m    echo "⚠️ $script not found"[0m
2025-10-14T16:29:14.6937213Z [36;1m  fi[0m
2025-10-14T16:29:14.6937378Z [36;1mdone[0m
2025-10-14T16:29:14.6937546Z [36;1m[0m
2025-10-14T16:29:14.6937862Z [36;1mvalidation_report+="## Feedback System: $feedback_available/3 scripts available\n"[0m
2025-10-14T16:29:14.6938230Z [36;1m[0m
2025-10-14T16:29:14.6938423Z [36;1m# Enhanced data_loader validation[0m
2025-10-14T16:29:14.6938713Z [36;1mif [ -f "utils/data_loader.py" ]; then[0m
2025-10-14T16:29:14.6939001Z [36;1m  echo "✅ Found utils/data_loader.py"[0m
2025-10-14T16:29:14.6939238Z [36;1m  [0m
2025-10-14T16:29:14.6939415Z [36;1m  python << 'EOF'[0m
2025-10-14T16:29:14.6939626Z [36;1mimport sys[0m
2025-10-14T16:29:14.6939832Z [36;1msys.path.append('utils')[0m
2025-10-14T16:29:14.6940058Z [36;1mtry:[0m
2025-10-14T16:29:14.6940257Z [36;1m  from data_loader import load_contacts[0m
2025-10-14T16:29:14.6940601Z [36;1m  print('✅ data_loader.py with load_contacts function available')[0m
2025-10-14T16:29:14.6940931Z [36;1mexcept Exception as e:[0m
2025-10-14T16:29:14.6941173Z [36;1m  print('⚠️ data_loader warning:', e)[0m
2025-10-14T16:29:14.6941410Z [36;1mEOF[0m
2025-10-14T16:29:14.6941580Z [36;1m  [0m
2025-10-14T16:29:14.6941806Z [36;1m  validation_report+="## Data Loader: AVAILABLE\n"[0m
2025-10-14T16:29:14.6942090Z [36;1melse[0m
2025-10-14T16:29:14.6942345Z [36;1m  echo "⚠️ utils/data_loader.py not found - using fallback"[0m
2025-10-14T16:29:14.6942714Z [36;1m  validation_report+="## Data Loader: USING FALLBACK\n"[0m
2025-10-14T16:29:14.6943012Z [36;1mfi[0m
2025-10-14T16:29:14.6943178Z [36;1m[0m
2025-10-14T16:29:14.6943561Z [36;1mvalidation_report+="\n## Overall Validation: $([ $overall_status -eq 0 ] && echo 'PASSED' || echo 'FAILED')\n"[0m
2025-10-14T16:29:14.6944153Z [36;1m[0m
2025-10-14T16:29:14.6944376Z [36;1mecho "status=$overall_status" >> $GITHUB_OUTPUT[0m
2025-10-14T16:29:14.6944674Z [36;1mecho "report<<EOF" >> $GITHUB_OUTPUT[0m
2025-10-14T16:29:14.6944971Z [36;1mecho -e "$validation_report" >> $GITHUB_OUTPUT[0m
2025-10-14T16:29:14.6945250Z [36;1mecho "EOF" >> $GITHUB_OUTPUT[0m
2025-10-14T16:29:14.6974851Z shell: /usr/bin/bash -e {0}
2025-10-14T16:29:14.6975092Z env:
2025-10-14T16:29:14.6975284Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:14.6975558Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:14.6975961Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:14.6976177Z   PRODUCTION_MODE: true
2025-10-14T16:29:14.6976383Z   TRACKING_DIR: tracking
2025-10-14T16:29:14.6976598Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:14.6976852Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:14.6977081Z   CONTACTS_DIR: contacts
2025-10-14T16:29:14.6977286Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:14.6977567Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6977963Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:14.6978348Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6978688Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6979043Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:14.6979407Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:14.6979741Z   GOOGLE_APPLICATION_CREDENTIALS: /tmp/google_svc.json
2025-10-14T16:29:14.6980018Z ##[endgroup]
2025-10-14T16:29:14.7028807Z Running comprehensive system validation...
2025-10-14T16:29:14.7029394Z Checking for campaign system scripts...
2025-10-14T16:29:14.7030019Z ✅ Found utils/docx_parser.py
2025-10-14T16:29:15.1411932Z GitHub Actions email sender available
2025-10-14T16:29:15.1412444Z Using professional data_loader module
2025-10-14T16:29:15.1413192Z ✅ utils/docx_parser.py imports successfully
2025-10-14T16:29:15.1413692Z   - Script is executable as module
2025-10-14T16:29:15.1585581Z ✅ Found utils/email_feedback_injector.py
2025-10-14T16:29:15.1836522Z ✅ email_feedback_injector imports successfully
2025-10-14T16:29:15.1873437Z ✅ Found utils/docx_feedback_processor.py
2025-10-14T16:29:15.2630556Z ✅ docx_feedback_processor imports successfully
2025-10-14T16:29:15.2749066Z ✅ Found utils/reply_tracker.py
2025-10-14T16:29:15.3492136Z ✅ reply_tracker imports successfully
2025-10-14T16:29:15.3546030Z ✅ Found utils/data_loader.py
2025-10-14T16:29:15.3639029Z ⚠️ data_loader warning: cannot import name 'load_contacts' from 'data_loader' (/home/runner/work/email-campaign-manager/email-campaign-manager/utils/data_loader.py)
2025-10-14T16:29:15.3709134Z ##[group]Run echo "Comprehensive contact data source validation..."
2025-10-14T16:29:15.3709649Z [36;1mecho "Comprehensive contact data source validation..."[0m
2025-10-14T16:29:15.3709957Z [36;1m[0m
2025-10-14T16:29:15.3710137Z [36;1mREAL_DATA_FOUND=false[0m
2025-10-14T16:29:15.3710359Z [36;1mCONTACT_FILES_COUNT=0[0m
2025-10-14T16:29:15.3710561Z [36;1m[0m
2025-10-14T16:29:15.3710747Z [36;1mif [ -d "$CONTACTS_DIR" ]; then[0m
2025-10-14T16:29:15.3711067Z [36;1m  echo "Analyzing contacts directory: $PWD/$CONTACTS_DIR"[0m
2025-10-14T16:29:15.3711364Z [36;1m  [0m
2025-10-14T16:29:15.3711559Z [36;1m  # Comprehensive file type analysis[0m
2025-10-14T16:29:15.3711901Z [36;1m  URL_FILES=$(find "$CONTACTS_DIR" -name "*.url" 2>/dev/null | wc -l)[0m
2025-10-14T16:29:15.3712296Z [36;1m  CSV_FILES=$(find "$CONTACTS_DIR" -name "*.csv" 2>/dev/null | wc -l)[0m
2025-10-14T16:29:15.3712785Z [36;1m  EXCEL_FILES=$(find "$CONTACTS_DIR" -name "*.xlsx" -o -name "*.xls" 2>/dev/null | wc -l)[0m
2025-10-14T16:29:15.3713260Z [36;1m  JSON_FILES=$(find "$CONTACTS_DIR" -name "*.json" 2>/dev/null | wc -l)[0m
2025-10-14T16:29:15.3713670Z [36;1m  DOCX_FILES=$(find "$CONTACTS_DIR" -name "*.docx" 2>/dev/null | wc -l)[0m
2025-10-14T16:29:15.3714210Z [36;1m  [0m
2025-10-14T16:29:15.3714537Z [36;1m  CONTACT_FILES_COUNT=$((URL_FILES + CSV_FILES + EXCEL_FILES + JSON_FILES + DOCX_FILES))[0m
2025-10-14T16:29:15.3714902Z [36;1m  [0m
2025-10-14T16:29:15.3715110Z [36;1m  echo "Enhanced contact data source analysis:"[0m
2025-10-14T16:29:15.3715428Z [36;1m  echo "  - Google Sheets URLs (.url): $URL_FILES"[0m
2025-10-14T16:29:15.3715719Z [36;1m  echo "  - CSV files: $CSV_FILES"[0m
2025-10-14T16:29:15.3715986Z [36;1m  echo "  - Excel files: $EXCEL_FILES"[0m
2025-10-14T16:29:15.3716266Z [36;1m  echo "  - JSON files: $JSON_FILES"[0m
2025-10-14T16:29:15.3716761Z [36;1m  echo "  - DOCX files: $DOCX_FILES"[0m
2025-10-14T16:29:15.3717077Z [36;1m  echo "  - Total contact source files: $CONTACT_FILES_COUNT"[0m
2025-10-14T16:29:15.3717373Z [36;1m  [0m
2025-10-14T16:29:15.3717577Z [36;1m  if [ "$CONTACT_FILES_COUNT" -gt 0 ]; then[0m
2025-10-14T16:29:15.3717835Z [36;1m    REAL_DATA_FOUND=true[0m
2025-10-14T16:29:15.3718114Z [36;1m    echo "✅ REAL CONTACT DATA SOURCES DETECTED"[0m
2025-10-14T16:29:15.3718378Z [36;1m    [0m
2025-10-14T16:29:15.3718602Z [36;1m    # Enhanced Google Sheets connectivity testing[0m
2025-10-14T16:29:15.3718898Z [36;1m    if [ "$URL_FILES" -gt 0 ]; then[0m
2025-10-14T16:29:15.3719188Z [36;1m      echo "Testing Google Sheets connectivity..."[0m
2025-10-14T16:29:15.3719498Z [36;1m      for url_file in "$CONTACTS_DIR"/*.url; do[0m
2025-10-14T16:29:15.3719778Z [36;1m        if [ -f "$url_file" ]; then[0m
2025-10-14T16:29:15.3720048Z [36;1m          echo "Testing: $(basename "$url_file")"[0m
2025-10-14T16:29:15.3720339Z [36;1m          SHEETS_URL=$(head -1 "$url_file")[0m
2025-10-14T16:29:15.3720663Z [36;1m          if [[ "$SHEETS_URL" =~ docs\.google\.com/spreadsheets ]]; then[0m
2025-10-14T16:29:15.3721058Z [36;1m            SHEET_ID=$(echo "$SHEETS_URL" | grep -o '/d/[^/]*' | cut -d'/' -f3)[0m
2025-10-14T16:29:15.3721546Z [36;1m            CSV_URL="https://docs.google.com/spreadsheets/d/$SHEET_ID/export?format=csv&gid=0"[0m
2025-10-14T16:29:15.3722059Z [36;1m            HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$CSV_URL" --max-time 10)[0m
2025-10-14T16:29:15.3722439Z [36;1m            echo "    HTTP Status: $HTTP_STATUS"[0m
2025-10-14T16:29:15.3722718Z [36;1m            if [ "$HTTP_STATUS" = "200" ]; then[0m
2025-10-14T16:29:15.3722996Z [36;1m              echo "    ✅ Google Sheet accessible"[0m
2025-10-14T16:29:15.3723259Z [36;1m            else[0m
2025-10-14T16:29:15.3723491Z [36;1m              echo "    ⚠️ Google Sheet access issue"[0m
2025-10-14T16:29:15.3723758Z [36;1m            fi[0m
2025-10-14T16:29:15.3723943Z [36;1m          fi[0m
2025-10-14T16:29:15.3724336Z [36;1m        fi[0m
2025-10-14T16:29:15.3724681Z [36;1m      done[0m
2025-10-14T16:29:15.3724864Z [36;1m    fi[0m
2025-10-14T16:29:15.3725028Z [36;1m    [0m
2025-10-14T16:29:15.3725233Z [36;1m    # Sample contact data preview[0m
2025-10-14T16:29:15.3725505Z [36;1m    echo "Sample contact files detected:"[0m
2025-10-14T16:29:15.3725948Z [36;1m    find "$CONTACTS_DIR" -type f \( -name "*.csv" -o -name "*.xlsx" -o -name "*.url" \) | head -3 | while read file; do[0m
2025-10-14T16:29:15.3726379Z [36;1m      echo "  - $(basename "$file")"[0m
2025-10-14T16:29:15.3726615Z [36;1m    done[0m
2025-10-14T16:29:15.3726787Z [36;1m  else[0m
2025-10-14T16:29:15.3727003Z [36;1m    echo "⚠️ No contact data source files found"[0m
2025-10-14T16:29:15.3727264Z [36;1m  fi[0m
2025-10-14T16:29:15.3727427Z [36;1melse[0m
2025-10-14T16:29:15.3727688Z [36;1m  echo "❌ Contacts directory does not exist: $PWD/$CONTACTS_DIR"[0m
2025-10-14T16:29:15.3728017Z [36;1mfi[0m
2025-10-14T16:29:15.3728183Z [36;1m[0m
2025-10-14T16:29:15.3728432Z [36;1mecho "real_data_found=$REAL_DATA_FOUND" >> $GITHUB_OUTPUT[0m
2025-10-14T16:29:15.3728828Z [36;1mecho "contact_files_count=$CONTACT_FILES_COUNT" >> $GITHUB_OUTPUT[0m
2025-10-14T16:29:15.3761717Z shell: /usr/bin/bash -e {0}
2025-10-14T16:29:15.3761949Z env:
2025-10-14T16:29:15.3762138Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:15.3762416Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:15.3762677Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:15.3762889Z   PRODUCTION_MODE: true
2025-10-14T16:29:15.3763091Z   TRACKING_DIR: tracking
2025-10-14T16:29:15.3763307Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:15.3763557Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:15.3763790Z   CONTACTS_DIR: contacts
2025-10-14T16:29:15.3764236Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:15.3764531Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:15.3765087Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:15.3765480Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:15.3765821Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:15.3766164Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:15.3766505Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:15.3766852Z   GOOGLE_APPLICATION_CREDENTIALS: /tmp/google_svc.json
2025-10-14T16:29:15.3767143Z ##[endgroup]
2025-10-14T16:29:15.3816627Z Comprehensive contact data source validation...
2025-10-14T16:29:15.3818611Z Analyzing contacts directory: /home/runner/work/email-campaign-manager/email-campaign-manager/contacts
2025-10-14T16:29:15.3910673Z Enhanced contact data source analysis:
2025-10-14T16:29:15.3911165Z   - Google Sheets URLs (.url): 0
2025-10-14T16:29:15.3911552Z   - CSV files: 3
2025-10-14T16:29:15.3911880Z   - Excel files: 0
2025-10-14T16:29:15.3912192Z   - JSON files: 1
2025-10-14T16:29:15.3912500Z   - DOCX files: 0
2025-10-14T16:29:15.3912823Z   - Total contact source files: 4
2025-10-14T16:29:15.3913404Z ✅ REAL CONTACT DATA SOURCES DETECTED
2025-10-14T16:29:15.3913840Z Sample contact files detected:
2025-10-14T16:29:15.3938671Z   - banks_contacts_20250925_184246.csv
2025-10-14T16:29:15.3949992Z   - edu_adults_contacts_20251004_121252.csv
2025-10-14T16:29:15.3961227Z   - enhanced_test_contacts.csv
2025-10-14T16:29:15.3988292Z ##[group]Run echo "Running data pipeline diagnostics..."
2025-10-14T16:29:15.3988693Z [36;1mecho "Running data pipeline diagnostics..."[0m
2025-10-14T16:29:15.3989015Z [36;1mpython .github/scripts/diagnose_data.py[0m
2025-10-14T16:29:15.4017800Z shell: /usr/bin/bash -e {0}
2025-10-14T16:29:15.4018028Z env:
2025-10-14T16:29:15.4018210Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:15.4018482Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:15.4018748Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:15.4018947Z   PRODUCTION_MODE: true
2025-10-14T16:29:15.4019139Z   TRACKING_DIR: tracking
2025-10-14T16:29:15.4019356Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:15.4019609Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:15.4019842Z   CONTACTS_DIR: contacts
2025-10-14T16:29:15.4020038Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:15.4020316Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:15.4020731Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:15.4021115Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:15.4021452Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:15.4021796Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:15.4022139Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:15.4022478Z   GOOGLE_APPLICATION_CREDENTIALS: /tmp/google_svc.json
2025-10-14T16:29:15.4022753Z ##[endgroup]
2025-10-14T16:29:15.4069788Z Running data pipeline diagnostics...
2025-10-14T16:29:15.6788566Z === DATA PIPELINE DIAGNOSTIC ===
2025-10-14T16:29:15.6788895Z 
2025-10-14T16:29:15.6789457Z Working Directory: /home/runner/work/email-campaign-manager/email-campaign-manager
2025-10-14T16:29:15.6790005Z 
2025-10-14T16:29:15.6790163Z Contacts Directory: contacts
2025-10-14T16:29:15.6791076Z   ✓ Exists: /home/runner/work/email-campaign-manager/email-campaign-manager/contacts
2025-10-14T16:29:15.6791724Z   Total files: 10
2025-10-14T16:29:15.6792054Z     - csv (4096 bytes, readable: True)
2025-10-14T16:29:15.6792506Z     - suppression_log.jsonl (0 bytes, readable: True)
2025-10-14T16:29:15.6792972Z     - reply_log.jsonl (0 bytes, readable: True)
2025-10-14T16:29:15.6793379Z     - docx (4096 bytes, readable: True)
2025-10-14T16:29:15.6793817Z     - suppression_list.json (85 bytes, readable: True)
2025-10-14T16:29:15.6794626Z     - banks_contacts_20250925_184246.csv (244 bytes, readable: True)
2025-10-14T16:29:15.6795617Z     - edu_adults_contacts_20251004_121252.csv (887 bytes, readable: True)
2025-10-14T16:29:15.6796140Z     - urls (4096 bytes, readable: True)
2025-10-14T16:29:15.6796588Z     - enhanced_test_contacts.csv (392 bytes, readable: True)
2025-10-14T16:29:15.6797057Z     - excel (4096 bytes, readable: True)
2025-10-14T16:29:15.6797317Z 
2025-10-14T16:29:15.6797464Z Templates Directory: campaign-templates
2025-10-14T16:29:15.6798273Z   ✓ Exists: /home/runner/work/email-campaign-manager/email-campaign-manager/campaign-templates
2025-10-14T16:29:15.6798932Z     - education: 2 files
2025-10-14T16:29:15.6799247Z     - finance: 2 files
2025-10-14T16:29:15.6799549Z     - healthcare: 2 files
2025-10-14T16:29:15.6799861Z     - industry: 0 files
2025-10-14T16:29:15.6800175Z     - technology: 0 files
2025-10-14T16:29:15.6800483Z     - government: 0 files
2025-10-14T16:29:15.6800678Z 
2025-10-14T16:29:15.6800837Z Scheduled Directory: scheduled-campaigns
2025-10-14T16:29:15.6801624Z   ✓ Exists: /home/runner/work/email-campaign-manager/email-campaign-manager/scheduled-campaigns
2025-10-14T16:29:15.6802273Z   Total files: 2
2025-10-14T16:29:15.6802564Z     - test_campaign.json
2025-10-14T16:29:15.6802911Z     - enhanced_welcome_campaign.txt
2025-10-14T16:29:15.6803177Z 
2025-10-14T16:29:15.6803307Z === TESTING DATA LOADING ===
2025-10-14T16:29:15.6803527Z 
2025-10-14T16:29:15.6803713Z Testing CSV load: banks_contacts_20250925_184246.csv
2025-10-14T16:29:15.6805045Z   ✓ Loaded 1 rows, columns: ['name', 'rank/title', 'position', 'email', 'phone', 'organization', 'sector', 'address', 'source']
2025-10-14T16:29:15.6806788Z   Sample row: {'name': 'Peter Pan', 'rank/title': 'Manager', 'position': nan, 'email': 'alerts@modelphysmat.com', 'phone': '0345 734 5345', 'organization': 'Barclays Bank', 'sector': 'finance', 'address': 'Located in: Blenheim House, Address: 120 Moorgate, London EC2M 6UK', 'source': "Barclays's Agency.txt"}
2025-10-14T16:29:15.7181009Z ##[group]Run echo "Enhanced contact source analysis..."
2025-10-14T16:29:15.7181417Z [36;1mecho "Enhanced contact source analysis..."[0m
2025-10-14T16:29:15.7181743Z [36;1mbash .github/scripts/fix_contact_outputs.sh[0m
2025-10-14T16:29:15.7213938Z shell: /usr/bin/bash -e {0}
2025-10-14T16:29:15.7214385Z env:
2025-10-14T16:29:15.7214577Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:15.7214862Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:15.7215119Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:15.7215320Z   PRODUCTION_MODE: true
2025-10-14T16:29:15.7215516Z   TRACKING_DIR: tracking
2025-10-14T16:29:15.7215732Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:15.7215985Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:15.7216222Z   CONTACTS_DIR: contacts
2025-10-14T16:29:15.7216426Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:15.7216711Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:15.7217153Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:15.7217549Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:15.7217893Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:15.7218241Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:15.7218589Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:15.7218937Z   GOOGLE_APPLICATION_CREDENTIALS: /tmp/google_svc.json
2025-10-14T16:29:15.7219220Z   CONTACT_SOURCE_FILTER: 
2025-10-14T16:29:15.7219423Z ##[endgroup]
2025-10-14T16:29:15.7269412Z Enhanced contact source analysis...
2025-10-14T16:29:16.0155021Z Analyzing contacts from: contacts
2025-10-14T16:29:16.0155621Z Contact source filter: None
2025-10-14T16:29:16.0156208Z Professional data_loader not available, using enhanced fallback
2025-10-14T16:29:16.0156734Z Loading CSV: contacts/banks_contacts_20250925_184246.csv
2025-10-14T16:29:16.0157275Z Loading CSV: contacts/edu_adults_contacts_20251004_121252.csv
2025-10-14T16:29:16.0157729Z Loading CSV: contacts/enhanced_test_contacts.csv
2025-10-14T16:29:16.0158233Z 
2025-10-14T16:29:16.0158432Z Successfully loaded 9 contacts using enhanced_fallback_loader
2025-10-14T16:29:16.0158798Z Sources: 3
2025-10-14T16:29:16.0158998Z Domains: 6
2025-10-14T16:29:16.0159216Z Top domain: modelphysmat.com
2025-10-14T16:29:16.0159490Z Set GITHUB_OUTPUT count=9
2025-10-14T16:29:16.0159739Z Contact analysis complete:
2025-10-14T16:29:16.0160007Z   - Total contacts: 9
2025-10-14T16:29:16.0160238Z   - Sources: 3
2025-10-14T16:29:16.0160444Z   - Domains: 6
2025-10-14T16:29:16.0160673Z   - Top domain: modelphysmat.com
2025-10-14T16:29:16.0703256Z Contact count set to: 9
2025-10-14T16:29:16.0733125Z ##[group]Run echo "Enhanced campaign template and domain analysis..."
2025-10-14T16:29:16.0733603Z [36;1mecho "Enhanced campaign template and domain analysis..."[0m
2025-10-14T16:29:16.0734209Z [36;1mbash .github/scripts/fix_domain_outputs.sh[0m
2025-10-14T16:29:16.0766294Z shell: /usr/bin/bash -e {0}
2025-10-14T16:29:16.0766519Z env:
2025-10-14T16:29:16.0766719Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:16.0766997Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:16.0767259Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:16.0767459Z   PRODUCTION_MODE: true
2025-10-14T16:29:16.0767651Z   TRACKING_DIR: tracking
2025-10-14T16:29:16.0767871Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:16.0768120Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:16.0768356Z   CONTACTS_DIR: contacts
2025-10-14T16:29:16.0768559Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:16.0768830Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.0769251Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:16.0769635Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.0769972Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.0770317Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.0770660Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:16.0771002Z   GOOGLE_APPLICATION_CREDENTIALS: /tmp/google_svc.json
2025-10-14T16:29:16.0771278Z   TARGET_DOMAIN_FILTER: 
2025-10-14T16:29:16.0771470Z ##[endgroup]
2025-10-14T16:29:16.0821395Z Enhanced campaign template and domain analysis...
2025-10-14T16:29:16.1070013Z Analyzing enhanced template structure...
2025-10-14T16:29:16.1070559Z   - education: 1 templates (0 DOCX, 0 JSON, 1 TXT, 0 HTML)
2025-10-14T16:29:16.1070988Z   - finance: 1 templates (1 DOCX, 0 JSON, 0 TXT, 0 HTML)
2025-10-14T16:29:16.1071404Z   - healthcare: 1 templates (1 DOCX, 0 JSON, 0 TXT, 0 HTML)
2025-10-14T16:29:16.1071798Z   - industry: 0 templates (0 DOCX, 0 JSON, 0 TXT, 0 HTML)
2025-10-14T16:29:16.1072190Z   - technology: 0 templates (0 DOCX, 0 JSON, 0 TXT, 0 HTML)
2025-10-14T16:29:16.1072580Z   - government: 0 templates (0 DOCX, 0 JSON, 0 TXT, 0 HTML)
2025-10-14T16:29:16.1072925Z Set GITHUB_OUTPUT campaigns=3
2025-10-14T16:29:16.1073315Z Enhanced template analysis completed: 3 templates, 2 scheduled campaigns
2025-10-14T16:29:16.1073748Z Template variables detected in:
2025-10-14T16:29:16.1074357Z   - enhanced_welcome_campaign.txt: ['name', 'organization', 'name']...
2025-10-14T16:29:16.1300536Z Template count set to: 3
2025-10-14T16:29:16.1346294Z ##[group]Run echo "Checking if outputs were properly set..."
2025-10-14T16:29:16.1346719Z [36;1mecho "Checking if outputs were properly set..."[0m
2025-10-14T16:29:16.1347030Z [36;1mecho "Contact analysis output: 9"[0m
2025-10-14T16:29:16.1347300Z [36;1mecho "Domain analysis output: 3"[0m
2025-10-14T16:29:16.1347544Z [36;1m[0m
2025-10-14T16:29:16.1347721Z [36;1m# Also check the JSON files[0m
2025-10-14T16:29:16.1347989Z [36;1mif [ -f contact_analysis.json ]; then[0m
2025-10-14T16:29:16.1348267Z [36;1m  echo "Contact analysis JSON exists:"[0m
2025-10-14T16:29:16.1348834Z [36;1m  cat contact_analysis.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"Total contacts: {data.get('total_contacts', 0)}\")"[0m
2025-10-14T16:29:16.1349552Z [36;1mfi[0m
2025-10-14T16:29:16.1349719Z [36;1m[0m
2025-10-14T16:29:16.1349916Z [36;1mif [ -f domain_analysis.json ]; then[0m
2025-10-14T16:29:16.1350188Z [36;1m  echo "Domain analysis JSON exists:"[0m
2025-10-14T16:29:16.1350766Z [36;1m  cat domain_analysis.json | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"Total templates: {data.get('template_count', 0)}\")"[0m
2025-10-14T16:29:16.1351285Z [36;1mfi[0m
2025-10-14T16:29:16.1382450Z shell: /usr/bin/bash -e {0}
2025-10-14T16:29:16.1382684Z env:
2025-10-14T16:29:16.1382881Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:16.1383155Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:16.1383411Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:16.1383613Z   PRODUCTION_MODE: true
2025-10-14T16:29:16.1383810Z   TRACKING_DIR: tracking
2025-10-14T16:29:16.1384269Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:16.1384647Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:16.1385002Z   CONTACTS_DIR: contacts
2025-10-14T16:29:16.1385300Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:16.1385755Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.1386288Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:16.1386752Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.1387258Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.1387697Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.1398204Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:16.1398635Z   GOOGLE_APPLICATION_CREDENTIALS: /tmp/google_svc.json
2025-10-14T16:29:16.1398931Z ##[endgroup]
2025-10-14T16:29:16.1448462Z Checking if outputs were properly set...
2025-10-14T16:29:16.1448884Z Contact analysis output: 9
2025-10-14T16:29:16.1449111Z Domain analysis output: 3
2025-10-14T16:29:16.1449335Z Contact analysis JSON exists:
2025-10-14T16:29:16.1610290Z Total contacts: 9
2025-10-14T16:29:16.1638894Z Domain analysis JSON exists:
2025-10-14T16:29:16.1803685Z Total templates: 3
2025-10-14T16:29:16.1862469Z ##[group]Run echo "=== ENHANCED PRE-EXECUTION FILE SYSTEM VERIFICATION ==="
2025-10-14T16:29:16.1862984Z [36;1mecho "=== ENHANCED PRE-EXECUTION FILE SYSTEM VERIFICATION ==="[0m
2025-10-14T16:29:16.1863510Z [36;1mecho "Current working directory: $PWD"[0m
2025-10-14T16:29:16.1863855Z [36;1mecho "Environment: Production with Enhanced Validation"[0m
2025-10-14T16:29:16.1864355Z [36;1mecho ""[0m
2025-10-14T16:29:16.1864539Z [36;1m[0m
2025-10-14T16:29:16.1864749Z [36;1mecho "Contacts directory ($CONTACTS_DIR):"[0m
2025-10-14T16:29:16.1865037Z [36;1mif [ -d "$CONTACTS_DIR" ]; then[0m
2025-10-14T16:29:16.1865305Z [36;1m  ls -la "$CONTACTS_DIR"[0m
2025-10-14T16:29:16.1865625Z [36;1m  echo "Contact files count: $(ls -1 "$CONTACTS_DIR" | wc -l)"[0m
2025-10-14T16:29:16.1865946Z [36;1m  echo "File types:"[0m
2025-10-14T16:29:16.1866260Z [36;1m  echo "  - CSV: $(find "$CONTACTS_DIR" -name "*.csv" 2>/dev/null | wc -l)"[0m
2025-10-14T16:29:16.1866757Z [36;1m  echo "  - Excel: $(find "$CONTACTS_DIR" -name "*.xlsx" -o -name "*.xls" 2>/dev/null | wc -l)"[0m
2025-10-14T16:29:16.1867245Z [36;1m  echo "  - Google Sheets: $(find "$CONTACTS_DIR" -name "*.url" 2>/dev/null | wc -l)"[0m
2025-10-14T16:29:16.1867682Z [36;1m  echo "  - JSON: $(find "$CONTACTS_DIR" -name "*.json" 2>/dev/null | wc -l)"[0m
2025-10-14T16:29:16.1868005Z [36;1melse[0m
2025-10-14T16:29:16.1868220Z [36;1m  echo "❌ Contacts directory not found"[0m
2025-10-14T16:29:16.1868472Z [36;1mfi[0m
2025-10-14T16:29:16.1868639Z [36;1mecho ""[0m
2025-10-14T16:29:16.1868806Z [36;1m[0m
2025-10-14T16:29:16.1869052Z [36;1mecho "Scheduled campaigns directory ($SCHEDULED_DIR):"[0m
2025-10-14T16:29:16.1869371Z [36;1mif [ -d "$SCHEDULED_DIR" ]; then[0m
2025-10-14T16:29:16.1869621Z [36;1m  ls -la "$SCHEDULED_DIR"[0m
2025-10-14T16:29:16.1870096Z [36;1m  CAMPAIGN_COUNT=$(find "$SCHEDULED_DIR" -name "*.txt" -o -name "*.json" -o -name "*.html" -o -name "*.md" -o -name "*.docx" 2>/dev/null | wc -l)[0m
2025-10-14T16:29:16.1870832Z [36;1m  echo "Campaign files count: $CAMPAIGN_COUNT"[0m
2025-10-14T16:29:16.1871097Z [36;1m  [0m
2025-10-14T16:29:16.1871284Z [36;1m  # Enhanced content preview[0m
2025-10-14T16:29:16.1871542Z [36;1m  for file in "$SCHEDULED_DIR"/*; do[0m
2025-10-14T16:29:16.1871798Z [36;1m    if [ -f "$file" ]; then[0m
2025-10-14T16:29:16.1872085Z [36;1m      echo "Enhanced preview of $(basename "$file"):"[0m
2025-10-14T16:29:16.1872408Z [36;1m      echo "  File size: $(wc -c < "$file") bytes"[0m
2025-10-14T16:29:16.1872792Z [36;1m      echo "  Template variables: $(grep -o '{{[^}]*}}' "$file" 2>/dev/null | wc -l)"[0m
2025-10-14T16:29:16.1873151Z [36;1m      echo "  First 3 lines:"[0m
2025-10-14T16:29:16.1873400Z [36;1m      head -3 "$file" | sed 's/^/    /'[0m
2025-10-14T16:29:16.1873649Z [36;1m      echo "---"[0m
2025-10-14T16:29:16.1873847Z [36;1m    fi[0m
2025-10-14T16:29:16.1874202Z [36;1m  done[0m
2025-10-14T16:29:16.1874370Z [36;1melse[0m
2025-10-14T16:29:16.1874609Z [36;1m  echo "❌ Scheduled campaigns directory not found"[0m
2025-10-14T16:29:16.1874888Z [36;1mfi[0m
2025-10-14T16:29:16.1875056Z [36;1mecho ""[0m
2025-10-14T16:29:16.1875228Z [36;1m[0m
2025-10-14T16:29:16.1875455Z [36;1mecho "Enhanced tracking directory ($TRACKING_DIR):"[0m
2025-10-14T16:29:16.1875772Z [36;1mif [ -d "$TRACKING_DIR" ]; then[0m
2025-10-14T16:29:16.1876025Z [36;1m  ls -la "$TRACKING_DIR"[0m
2025-10-14T16:29:16.1876280Z [36;1m  echo "Tracking subdirectories:"[0m
2025-10-14T16:29:16.1876569Z [36;1m  find "$TRACKING_DIR" -type d | sed 's/^/  - /'[0m
2025-10-14T16:29:16.1876839Z [36;1melse[0m
2025-10-14T16:29:16.1877041Z [36;1m  echo "❌ Tracking directory not found"[0m
2025-10-14T16:29:16.1877289Z [36;1mfi[0m
2025-10-14T16:29:16.1907688Z shell: /usr/bin/bash -e {0}
2025-10-14T16:29:16.1907920Z env:
2025-10-14T16:29:16.1908112Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:16.1908402Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:16.1908821Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:16.1909034Z   PRODUCTION_MODE: true
2025-10-14T16:29:16.1909232Z   TRACKING_DIR: tracking
2025-10-14T16:29:16.1909448Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:16.1909696Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:16.1909936Z   CONTACTS_DIR: contacts
2025-10-14T16:29:16.1910141Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:16.1910425Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.1910834Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:16.1911214Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.1911556Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.1911900Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.1912251Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:16.1912597Z   GOOGLE_APPLICATION_CREDENTIALS: /tmp/google_svc.json
2025-10-14T16:29:16.1912871Z ##[endgroup]
2025-10-14T16:29:16.1961683Z === ENHANCED PRE-EXECUTION FILE SYSTEM VERIFICATION ===
2025-10-14T16:29:16.1962208Z Current working directory: /home/runner/work/email-campaign-manager/email-campaign-manager
2025-10-14T16:29:16.1962680Z Environment: Production with Enhanced Validation
2025-10-14T16:29:16.1962879Z 
2025-10-14T16:29:16.1962975Z Contacts directory (contacts):
2025-10-14T16:29:16.1976406Z total 40
2025-10-14T16:29:16.1976681Z drwxr-xr-x  6 runner runner 4096 Oct 14 16:29 .
2025-10-14T16:29:16.1976994Z drwxr-xr-x 12 runner runner 4096 Oct 14 16:29 ..
2025-10-14T16:29:16.1977372Z -rw-r--r--  1 runner runner  244 Oct 14 16:28 banks_contacts_20250925_184246.csv
2025-10-14T16:29:16.1977750Z drwxr-xr-x  2 runner runner 4096 Oct 14 16:29 csv
2025-10-14T16:29:16.1978046Z drwxr-xr-x  2 runner runner 4096 Oct 14 16:29 docx
2025-10-14T16:29:16.1978410Z -rw-r--r--  1 runner runner  887 Oct 14 16:28 edu_adults_contacts_20251004_121252.csv
2025-10-14T16:29:16.1979049Z -rw-r--r--  1 runner runner  392 Oct 14 16:29 enhanced_test_contacts.csv
2025-10-14T16:29:16.1979407Z drwxr-xr-x  2 runner runner 4096 Oct 14 16:29 excel
2025-10-14T16:29:16.1979735Z -rw-r--r--  1 runner runner    0 Oct 14 16:28 reply_log.jsonl
2025-10-14T16:29:16.1980092Z -rw-r--r--  1 runner runner   85 Oct 14 16:28 suppression_list.json
2025-10-14T16:29:16.1980457Z -rw-r--r--  1 runner runner    0 Oct 14 16:28 suppression_log.jsonl
2025-10-14T16:29:16.1980788Z drwxr-xr-x  2 runner runner 4096 Oct 14 16:29 urls
2025-10-14T16:29:16.1998285Z Contact files count: 10
2025-10-14T16:29:16.1998634Z File types:
2025-10-14T16:29:16.2017903Z   - CSV: 3
2025-10-14T16:29:16.2036988Z   - Excel: 0
2025-10-14T16:29:16.2055621Z   - Google Sheets: 0
2025-10-14T16:29:16.2074249Z   - JSON: 1
2025-10-14T16:29:16.2074448Z 
2025-10-14T16:29:16.2074803Z Scheduled campaigns directory (scheduled-campaigns):
2025-10-14T16:29:16.2086859Z total 16
2025-10-14T16:29:16.2087152Z drwxr-xr-x  2 runner runner 4096 Oct 14 16:29 .
2025-10-14T16:29:16.2087487Z drwxr-xr-x 12 runner runner 4096 Oct 14 16:29 ..
2025-10-14T16:29:16.2087852Z -rw-r--r--  1 runner runner  250 Oct 14 16:29 enhanced_welcome_campaign.txt
2025-10-14T16:29:16.2088262Z -rw-r--r--  1 runner runner 2730 Oct 14 16:28 test_campaign.json
2025-10-14T16:29:16.2107950Z Campaign files count: 2
2025-10-14T16:29:16.2120333Z Enhanced preview of enhanced_welcome_campaign.txt:
2025-10-14T16:29:16.2135325Z   File size: 250 bytes
2025-10-14T16:29:16.2154905Z   Template variables: 6
2025-10-14T16:29:16.2156648Z   First 3 lines:
2025-10-14T16:29:16.2170759Z     Subject: Welcome {{name}} from {{organization}} to Our Platform!
2025-10-14T16:29:16.2171275Z     
2025-10-14T16:29:16.2171465Z     Dear {{name}},
2025-10-14T16:29:16.2172382Z ---
2025-10-14T16:29:16.2184681Z Enhanced preview of test_campaign.json:
2025-10-14T16:29:16.2199682Z   File size: 2730 bytes
2025-10-14T16:29:16.2218388Z   Template variables: 0
2025-10-14T16:29:16.2218762Z   First 3 lines:
2025-10-14T16:29:16.2232019Z     {
2025-10-14T16:29:16.2232608Z       "name": "Education Outreach Campaign",
2025-10-14T16:29:16.2233068Z       "sector": "education",
2025-10-14T16:29:16.2234373Z ---
2025-10-14T16:29:16.2234541Z 
2025-10-14T16:29:16.2234703Z Enhanced tracking directory (tracking):
2025-10-14T16:29:16.2247302Z total 40
2025-10-14T16:29:16.2247542Z drwxr-xr-x  8 runner runner 4096 Oct 14 16:29 .
2025-10-14T16:29:16.2247860Z drwxr-xr-x 12 runner runner 4096 Oct 14 16:29 ..
2025-10-14T16:29:16.2248176Z -rw-r--r--  1 runner runner    0 Oct 14 16:28 .gitkeep
2025-10-14T16:29:16.2248517Z drwxr-xr-x  2 runner runner 4096 Oct 14 16:29 batch_reports
2025-10-14T16:29:16.2248847Z drwxr-xr-x  3 runner runner 4096 Oct 14 16:28 default
2025-10-14T16:29:16.2249334Z drwxr-xr-x  2 runner runner 4096 Oct 14 16:29 domain_stats
2025-10-14T16:29:16.2249697Z drwxr-xr-x  2 runner runner 4096 Oct 14 16:29 execution_logs
2025-10-14T16:29:16.2250124Z drwxr-xr-x  2 runner runner 4096 Oct 14 16:29 feedback_responses
2025-10-14T16:29:16.2250723Z -rw-r--r--  1 runner runner  142 Oct 14 16:28 rate_limits.json
2025-10-14T16:29:16.2251306Z drwxr-xr-x  2 runner runner 4096 Oct 14 16:29 reply_tracking
2025-10-14T16:29:16.2251890Z -rw-r--r--  1 runner runner  142 Oct 14 16:28 unsubscribed.json
2025-10-14T16:29:16.2252392Z Tracking subdirectories:
2025-10-14T16:29:16.2263622Z   - tracking
2025-10-14T16:29:16.2264397Z   - tracking/domain_stats
2025-10-14T16:29:16.2264776Z   - tracking/default
2025-10-14T16:29:16.2265132Z   - tracking/default/campaigns
2025-10-14T16:29:16.2265506Z   - tracking/execution_logs
2025-10-14T16:29:16.2265858Z   - tracking/feedback_responses
2025-10-14T16:29:16.2266218Z   - tracking/batch_reports
2025-10-14T16:29:16.2266443Z   - tracking/reply_tracking
2025-10-14T16:29:16.2312871Z ##[group]Run actions/upload-artifact@v4
2025-10-14T16:29:16.2313133Z with:
2025-10-14T16:29:16.2313351Z   name: enhanced-validation-results-18503360273
2025-10-14T16:29:16.2313835Z   path: contact_analysis.json
domain_analysis.json
*.log

2025-10-14T16:29:16.2314387Z   retention-days: 7
2025-10-14T16:29:16.2314586Z   if-no-files-found: warn
2025-10-14T16:29:16.2314789Z   compression-level: 6
2025-10-14T16:29:16.2314985Z   overwrite: false
2025-10-14T16:29:16.2315181Z   include-hidden-files: false
2025-10-14T16:29:16.2315392Z env:
2025-10-14T16:29:16.2315572Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:16.2315847Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:16.2316102Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:16.2316302Z   PRODUCTION_MODE: true
2025-10-14T16:29:16.2316499Z   TRACKING_DIR: tracking
2025-10-14T16:29:16.2316717Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:16.2316970Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:16.2317235Z   CONTACTS_DIR: contacts
2025-10-14T16:29:16.2317438Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:16.2317717Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.2318109Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:16.2318505Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.2318854Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.2319202Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.2319556Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:16.2319906Z   GOOGLE_APPLICATION_CREDENTIALS: /tmp/google_svc.json
2025-10-14T16:29:16.2320186Z ##[endgroup]
2025-10-14T16:29:16.4454466Z With the provided path, there will be 3 files uploaded
2025-10-14T16:29:16.4458916Z Artifact name is valid!
2025-10-14T16:29:16.4460828Z Root directory input is valid!
2025-10-14T16:29:16.5636531Z Beginning upload of artifact content to blob storage
2025-10-14T16:29:16.6300294Z Uploaded bytes 1356
2025-10-14T16:29:16.6489947Z Finished uploading artifact content to blob storage!
2025-10-14T16:29:16.6493502Z SHA256 digest of uploaded artifact zip is bf795ba00f21a52dd5ed6a608029ff838b2fb1d53db9d3ed72043741df510721
2025-10-14T16:29:16.6495464Z Finalizing artifact upload
2025-10-14T16:29:16.7329217Z Artifact enhanced-validation-results-18503360273.zip successfully finalized. Artifact ID 4267509952
2025-10-14T16:29:16.7330544Z Artifact enhanced-validation-results-18503360273 has been successfully uploaded! Final size is 1356 bytes. Artifact ID is 4267509952
2025-10-14T16:29:16.7336821Z Artifact download URL: https://github.com/sednabcn/email-campaign-manager/actions/runs/18503360273/artifacts/4267509952
2025-10-14T16:29:16.7432270Z ##[group]Run echo "### Enhanced Validation Summary" >> $GITHUB_STEP_SUMMARY
2025-10-14T16:29:16.7432763Z [36;1mecho "### Enhanced Validation Summary" >> $GITHUB_STEP_SUMMARY[0m
2025-10-14T16:29:16.7433126Z [36;1mecho "" >> $GITHUB_STEP_SUMMARY[0m
2025-10-14T16:29:16.7433420Z [36;1mecho "# Enhanced System Validation Report[0m
2025-10-14T16:29:16.7433690Z [36;1m[0m
2025-10-14T16:29:16.7433896Z [36;1m## Main Campaign Processor: PASSED[0m
2025-10-14T16:29:16.7434471Z [36;1m## Feedback System: 3/3 scripts available[0m
2025-10-14T16:29:16.7434748Z [36;1m## Data Loader: AVAILABLE[0m
2025-10-14T16:29:16.7434976Z [36;1m[0m
2025-10-14T16:29:16.7435164Z [36;1m## Overall Validation: PASSED[0m
2025-10-14T16:29:16.7435421Z [36;1m" >> $GITHUB_STEP_SUMMARY[0m
2025-10-14T16:29:16.7435664Z [36;1mecho "" >> $GITHUB_STEP_SUMMARY[0m
2025-10-14T16:29:16.7435979Z [36;1mecho "**Real Data Sources:** true" >> $GITHUB_STEP_SUMMARY[0m
2025-10-14T16:29:16.7436378Z [36;1mecho "**Contact Files Found:** 4" >> $GITHUB_STEP_SUMMARY[0m
2025-10-14T16:29:16.7436751Z [36;1mecho "**Contacts Loaded:** 9" >> $GITHUB_STEP_SUMMARY[0m
2025-10-14T16:29:16.7437116Z [36;1mecho "**Campaign Templates:** 3" >> $GITHUB_STEP_SUMMARY[0m
2025-10-14T16:29:16.7437429Z [36;1mecho "" >> $GITHUB_STEP_SUMMARY[0m
2025-10-14T16:29:16.7437663Z [36;1m[0m
2025-10-14T16:29:16.7437930Z [36;1m# Add this as a new step BEFORE your existing campaign execution step[0m
2025-10-14T16:29:16.7471253Z shell: /usr/bin/bash -e {0}
2025-10-14T16:29:16.7471498Z env:
2025-10-14T16:29:16.7471699Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:16.7471991Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:16.7472260Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:16.7472478Z   PRODUCTION_MODE: true
2025-10-14T16:29:16.7472687Z   TRACKING_DIR: tracking
2025-10-14T16:29:16.7472913Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:16.7473174Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:16.7473416Z   CONTACTS_DIR: contacts
2025-10-14T16:29:16.7473630Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:16.7473927Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.7474554Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:16.7474946Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.7475295Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.7475653Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.7476008Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:16.7476359Z   GOOGLE_APPLICATION_CREDENTIALS: /tmp/google_svc.json
2025-10-14T16:29:16.7476640Z ##[endgroup]
2025-10-14T16:29:16.7560009Z ##[group]Run echo "🔒 Running Enhanced Compliance Checks..."
2025-10-14T16:29:16.7560475Z [36;1mecho "🔒 Running Enhanced Compliance Checks..."[0m
2025-10-14T16:29:16.7560813Z [36;1mecho "========================================"[0m
2025-10-14T16:29:16.7561084Z [36;1m[0m
2025-10-14T16:29:16.7561281Z [36;1m# Ensure directories exist[0m
2025-10-14T16:29:16.7561542Z [36;1mmkdir -p contacts tracking[0m
2025-10-14T16:29:16.7561779Z [36;1m[0m
2025-10-14T16:29:16.7561992Z [36;1m# STEP 1: Load/Create suppression list[0m
2025-10-14T16:29:16.7562312Z [36;1mecho "📋 Step 1: Loading suppression list..."[0m
2025-10-14T16:29:16.7562642Z [36;1mif [ -f contacts/suppression_list.json ]; then[0m
2025-10-14T16:29:16.7562977Z [36;1m   echo "✅ Found existing suppression list:"[0m
2025-10-14T16:29:16.7563344Z [36;1m   cat contacts/suppression_list.json | python3 -m json.tool[0m
2025-10-14T16:29:16.7563670Z [36;1melse[0m
2025-10-14T16:29:16.7563915Z [36;1m   echo "Creating new suppression list..."[0m
2025-10-14T16:29:16.7564453Z [36;1m   cat > contacts/suppression_list.json << 'EOF'[0m
2025-10-14T16:29:16.7564728Z [36;1m   {[0m
2025-10-14T16:29:16.7564921Z [36;1m   "suppressed_emails": [],[0m
2025-10-14T16:29:16.7565195Z [36;1m   "last_updated": "$(date -Iseconds)",[0m
2025-10-14T16:29:16.7565477Z [36;1m   "count": 0[0m
2025-10-14T16:29:16.7565683Z [36;1m   }[0m
2025-10-14T16:29:16.7565861Z [36;1mEOF[0m
2025-10-14T16:29:16.7566082Z [36;1mecho "✅ Created empty suppression list"[0m
2025-10-14T16:29:16.7566348Z [36;1mfi[0m
2025-10-14T16:29:16.7566526Z [36;1m[0m
2025-10-14T16:29:16.7566794Z [36;1m# STEP 2: Check for unsubscribe requests (if IMAP configured)[0m
2025-10-14T16:29:16.7567121Z [36;1mecho ""[0m
2025-10-14T16:29:16.7567378Z [36;1mecho "📧 Step 2: Checking for unsubscribe requests..."[0m
2025-10-14T16:29:16.7567685Z [36;1mif [ -n "" ]; then[0m
2025-10-14T16:29:16.7568049Z [36;1m   python utils/reply_handler.py --days 7 || echo "⚠️  Reply checking skipped"[0m
2025-10-14T16:29:16.7568423Z [36;1melse[0m
2025-10-14T16:29:16.7568672Z [36;1m   echo "⚠️  IMAP not configured - skipping reply check"[0m
2025-10-14T16:29:16.7568965Z [36;1mfi[0m
2025-10-14T16:29:16.7569136Z [36;1m[0m
2025-10-14T16:29:16.7569339Z [36;1m# STEP 3: Show current compliance stats[0m
2025-10-14T16:29:16.7569601Z [36;1mecho ""[0m
2025-10-14T16:29:16.7569834Z [36;1mecho "📊 Step 3: Current Compliance Status..."[0m
2025-10-14T16:29:16.7570124Z [36;1mpython3 << 'PYEOF'[0m
2025-10-14T16:29:16.7570401Z [36;1mfrom compliance_wrapper import MinimalCompliance[0m
2025-10-14T16:29:16.7570692Z [36;1m[0m
2025-10-14T16:29:16.7570888Z [36;1mcompliance = MinimalCompliance([0m
2025-10-14T16:29:16.7571329Z [36;1mdaily_limit=int('50' or 50),[0m
2025-10-14T16:29:16.7571574Z [36;1mper_domain_limit=5[0m
2025-10-14T16:29:16.7571791Z [36;1m)[0m
2025-10-14T16:29:16.7571959Z [36;1m[0m
2025-10-14T16:29:16.7572143Z [36;1mstats = compliance.get_stats()[0m
2025-10-14T16:29:16.7572387Z [36;1m[0m
2025-10-14T16:29:16.7572620Z [36;1mprint("\n📊 Compliance Statistics:")[0m
2025-10-14T16:29:16.7572974Z [36;1mprint(f"   Suppressed emails: {stats['suppressed_count']}")[0m
2025-10-14T16:29:16.7573383Z [36;1mprint(f"   Sent today: {stats['sent_today']}/{stats['daily_limit']}")[0m
2025-10-14T16:29:16.7573779Z [36;1mprint(f"   Remaining today: {stats['remaining_today']}")[0m
2025-10-14T16:29:16.7574334Z [36;1mprint(f"   Domains contacted: {stats['domains_contacted']}")[0m
2025-10-14T16:29:16.7574728Z [36;1mprint(f"   Per-domain limit: {stats['per_domain_limit']}")[0m
2025-10-14T16:29:16.7575030Z [36;1m[0m
2025-10-14T16:29:16.7575209Z [36;1m# Check capacity[0m
2025-10-14T16:29:16.7575452Z [36;1mif not compliance.can_send_today():[0m
2025-10-14T16:29:16.7575787Z [36;1m  print("\n⚠️  WARNING: Daily send limit reached!")[0m
2025-10-14T16:29:16.7576123Z [36;1m  print("   No more emails can be sent today")[0m
2025-10-14T16:29:16.7576392Z [36;1m[0m
2025-10-14T16:29:16.7576763Z [36;1mif stats['remaining_today'] < 10:[0m
2025-10-14T16:29:16.7577147Z [36;1m  print(f"\n⚠️  WARNING: Only {stats['remaining_today']} sends remaining today")[0m
2025-10-14T16:29:16.7577499Z [36;1m[0m
2025-10-14T16:29:16.7577707Z [36;1mprint("\n✅ Compliance check complete")[0m
2025-10-14T16:29:16.7577971Z [36;1mPYEOF[0m
2025-10-14T16:29:16.7578143Z [36;1m[0m
2025-10-14T16:29:16.7578329Z [36;1m# STEP 4: Validate contacts file[0m
2025-10-14T16:29:16.7578575Z [36;1mecho ""[0m
2025-10-14T16:29:16.7578810Z [36;1mecho "📄 Step 4: Validating contacts file..."[0m
2025-10-14T16:29:16.7579105Z [36;1mCONTACTS_FILE="contact_details/"[0m
2025-10-14T16:29:16.7579377Z [36;1mif [ ! -f "$CONTACTS_FILE" ]; then[0m
2025-10-14T16:29:16.7579700Z [36;1m   echo "⚠️  Contacts file not found: $CONTACTS_FILE"[0m
2025-10-14T16:29:16.7580010Z [36;1m   echo "Available files:"[0m
2025-10-14T16:29:16.7580315Z [36;1m   ls -lh contacts/ || echo "contacts/ directory not found"[0m
2025-10-14T16:29:16.7580615Z [36;1melse[0m
2025-10-14T16:29:16.7580842Z [36;1m   echo "✅ Contacts file found: $CONTACTS_FILE"[0m
2025-10-14T16:29:16.7581110Z [36;1m[0m
2025-10-14T16:29:16.7581292Z [36;1m   # Show sample (first 3 lines)[0m
2025-10-14T16:29:16.7581551Z [36;1m   echo "Sample contacts:"[0m
2025-10-14T16:29:16.7581801Z [36;1m   head -3 "$CONTACTS_FILE"[0m
2025-10-14T16:29:16.7582030Z [36;1mfi[0m
2025-10-14T16:29:16.7582199Z [36;1m[0m
2025-10-14T16:29:16.7582367Z [36;1mecho ""[0m
2025-10-14T16:29:16.7582586Z [36;1mecho "========================================"[0m
2025-10-14T16:29:16.7582910Z [36;1mecho "✅ Pre-flight compliance checks complete"[0m
2025-10-14T16:29:16.7611561Z shell: /usr/bin/bash -e {0}
2025-10-14T16:29:16.7611792Z env:
2025-10-14T16:29:16.7611995Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:16.7612280Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:16.7612546Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:16.7612757Z   PRODUCTION_MODE: true
2025-10-14T16:29:16.7612969Z   TRACKING_DIR: tracking
2025-10-14T16:29:16.7613196Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:16.7613455Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:16.7613690Z   CONTACTS_DIR: contacts
2025-10-14T16:29:16.7613898Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:16.7614354Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.7614765Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:16.7615160Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.7615504Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.7615854Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.7616356Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:16.7616703Z   GOOGLE_APPLICATION_CREDENTIALS: /tmp/google_svc.json
2025-10-14T16:29:16.7616985Z ##[endgroup]
2025-10-14T16:29:16.7664133Z 🔒 Running Enhanced Compliance Checks...
2025-10-14T16:29:16.7664520Z ========================================
2025-10-14T16:29:16.7677093Z 📋 Step 1: Loading suppression list...
2025-10-14T16:29:16.7677435Z ✅ Found existing suppression list:
2025-10-14T16:29:16.8304855Z {
2025-10-14T16:29:16.8305284Z     "suppressed_emails": [],
2025-10-14T16:29:16.8305794Z     "last_updated": "2025-10-09T16:00:00",
2025-10-14T16:29:16.8306279Z     "count": 0
2025-10-14T16:29:16.8306604Z }
2025-10-14T16:29:16.8352329Z 
2025-10-14T16:29:16.8352992Z 📧 Step 2: Checking for unsubscribe requests...
2025-10-14T16:29:16.8353654Z ⚠️  IMAP not configured - skipping reply check
2025-10-14T16:29:16.8353917Z 
2025-10-14T16:29:16.8354396Z 📊 Step 3: Current Compliance Status...
2025-10-14T16:29:16.8638499Z ✅ Compliance initialized:
2025-10-14T16:29:16.8638992Z    Suppressed: 0
2025-10-14T16:29:16.8639319Z    Sent today: 0/50
2025-10-14T16:29:16.8639652Z    Min delay: 30s between sends
2025-10-14T16:29:16.8639935Z 
2025-10-14T16:29:16.8640192Z 📊 Compliance Statistics:
2025-10-14T16:29:16.8640826Z    Suppressed emails: 0
2025-10-14T16:29:16.8641096Z    Sent today: 0/50
2025-10-14T16:29:16.8641336Z    Remaining today: 50
2025-10-14T16:29:16.8641589Z    Domains contacted: 0
2025-10-14T16:29:16.8641834Z    Per-domain limit: 5
2025-10-14T16:29:16.8641982Z 
2025-10-14T16:29:16.8642137Z ✅ Compliance check complete
2025-10-14T16:29:16.8669829Z 
2025-10-14T16:29:16.8670261Z 📄 Step 4: Validating contacts file...
2025-10-14T16:29:16.8670844Z ⚠️  Contacts file not found: contact_details/
2025-10-14T16:29:16.8671287Z Available files:
2025-10-14T16:29:16.8684908Z total 32K
2025-10-14T16:29:16.8685325Z -rw-r--r-- 1 runner runner  244 Oct 14 16:28 banks_contacts_20250925_184246.csv
2025-10-14T16:29:16.8685743Z drwxr-xr-x 2 runner runner 4.0K Oct 14 16:29 csv
2025-10-14T16:29:16.8686069Z drwxr-xr-x 2 runner runner 4.0K Oct 14 16:29 docx
2025-10-14T16:29:16.8686443Z -rw-r--r-- 1 runner runner  887 Oct 14 16:28 edu_adults_contacts_20251004_121252.csv
2025-10-14T16:29:16.8687118Z -rw-r--r-- 1 runner runner  392 Oct 14 16:29 enhanced_test_contacts.csv
2025-10-14T16:29:16.8687700Z drwxr-xr-x 2 runner runner 4.0K Oct 14 16:29 excel
2025-10-14T16:29:16.8688178Z -rw-r--r-- 1 runner runner    0 Oct 14 16:28 reply_log.jsonl
2025-10-14T16:29:16.8688546Z -rw-r--r-- 1 runner runner   85 Oct 14 16:28 suppression_list.json
2025-10-14T16:29:16.8689028Z -rw-r--r-- 1 runner runner    0 Oct 14 16:28 suppression_log.jsonl
2025-10-14T16:29:16.8689624Z drwxr-xr-x 2 runner runner 4.0K Oct 14 16:29 urls
2025-10-14T16:29:16.8689951Z 
2025-10-14T16:29:16.8690076Z ========================================
2025-10-14T16:29:16.8690620Z ✅ Pre-flight compliance checks complete
2025-10-14T16:29:16.8716928Z ##[group]Run echo "🔒 Running Integrated Campaign with Compliance..."
2025-10-14T16:29:16.8717419Z [36;1mecho "🔒 Running Integrated Campaign with Compliance..."[0m
2025-10-14T16:29:16.8717750Z [36;1mecho "📋 Configuration:"[0m
2025-10-14T16:29:16.8718012Z [36;1mecho "  - Dry Run: $DRY_RUN_MODE"[0m
2025-10-14T16:29:16.8718291Z [36;1mecho "  - Daily Limit: $DAILY_LIMIT"[0m
2025-10-14T16:29:16.8718602Z [36;1mecho "  - Per-Domain Limit: $PER_DOMAIN_LIMIT"[0m
2025-10-14T16:29:16.8718889Z [36;1mecho ""[0m
2025-10-14T16:29:16.8719073Z [36;1m[0m
2025-10-14T16:29:16.8719264Z [36;1m# Build command arguments array[0m
2025-10-14T16:29:16.8719505Z [36;1mARGS=([0m
2025-10-14T16:29:16.8719699Z [36;1m  --contacts "contacts"[0m
2025-10-14T16:29:16.8719970Z [36;1m  --scheduled "scheduled-campaigns"[0m
2025-10-14T16:29:16.8720249Z [36;1m  --tracking "tracking"[0m
2025-10-14T16:29:16.8720513Z [36;1m  --templates "campaign-templates"[0m
2025-10-14T16:29:16.8720825Z [36;1m  --alerts "alerts@modelphysmat.com"[0m
2025-10-14T16:29:16.8721078Z [36;1m)[0m
2025-10-14T16:29:16.8721428Z [36;1m[0m
2025-10-14T16:29:16.8721665Z [36;1m# Conditionally add --dry-run flag (only when true)[0m
2025-10-14T16:29:16.8721992Z [36;1mif [ "$DRY_RUN_MODE" == "true" ]; then[0m
2025-10-14T16:29:16.8722261Z [36;1m  ARGS+=(--dry-run)[0m
2025-10-14T16:29:16.8722547Z [36;1m  echo "🧪 DRY-RUN MODE: Simulating campaign execution"[0m
2025-10-14T16:29:16.8722842Z [36;1melse[0m
2025-10-14T16:29:16.8723078Z [36;1m  echo "📤 LIVE MODE: Executing actual campaign"[0m
2025-10-14T16:29:16.8723355Z [36;1mfi[0m
2025-10-14T16:29:16.8723529Z [36;1m[0m
2025-10-14T16:29:16.8723717Z [36;1m# Execute integrated runner[0m
2025-10-14T16:29:16.8724137Z [36;1mecho ""[0m
2025-10-14T16:29:16.8724512Z [36;1mecho "Executing: python utils/integrated_runner.py ${ARGS[@]}"[0m
2025-10-14T16:29:16.8724853Z [36;1mecho ""[0m
2025-10-14T16:29:16.8725037Z [36;1m[0m
2025-10-14T16:29:16.8725279Z [36;1mpython utils/integrated_runner.py "${ARGS[@]}"[0m
2025-10-14T16:29:16.8725569Z [36;1m[0m
2025-10-14T16:29:16.8725753Z [36;1mEXIT_CODE=$?[0m
2025-10-14T16:29:16.8725956Z [36;1mecho ""[0m
2025-10-14T16:29:16.8726152Z [36;1mecho "Exit code: $EXIT_CODE"[0m
2025-10-14T16:29:16.8726392Z [36;1m[0m
2025-10-14T16:29:16.8726570Z [36;1mif [ $EXIT_CODE -eq 0 ]; then[0m
2025-10-14T16:29:16.8726879Z [36;1m  echo "✅ Campaign execution completed successfully"[0m
2025-10-14T16:29:16.8727175Z [36;1melse[0m
2025-10-14T16:29:16.8727383Z [36;1m  echo "❌ Campaign execution failed"[0m
2025-10-14T16:29:16.8727648Z [36;1m  exit $EXIT_CODE[0m
2025-10-14T16:29:16.8727856Z [36;1mfi[0m
2025-10-14T16:29:16.8759427Z shell: /usr/bin/bash -e {0}
2025-10-14T16:29:16.8759657Z env:
2025-10-14T16:29:16.8759854Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:16.8760135Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:16.8760398Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:16.8760607Z   PRODUCTION_MODE: true
2025-10-14T16:29:16.8760822Z   TRACKING_DIR: tracking
2025-10-14T16:29:16.8761052Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:16.8761324Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:16.8761570Z   CONTACTS_DIR: contacts
2025-10-14T16:29:16.8761783Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:16.8762071Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.8762468Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:16.8762862Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.8763214Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.8763569Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:16.8763920Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:16.8764511Z   GOOGLE_APPLICATION_CREDENTIALS: /tmp/google_svc.json
2025-10-14T16:29:16.8764795Z   DRY_RUN_MODE: false
2025-10-14T16:29:16.8765001Z   COMPLIANCE_MODE: true
2025-10-14T16:29:16.8765382Z   DAILY_LIMIT: 50
2025-10-14T16:29:16.8765585Z   PER_DOMAIN_LIMIT: 5
2025-10-14T16:29:16.8765798Z ##[endgroup]
2025-10-14T16:29:16.8814807Z 🔒 Running Integrated Campaign with Compliance...
2025-10-14T16:29:16.8815341Z 📋 Configuration:
2025-10-14T16:29:16.8815668Z   - Dry Run: false
2025-10-14T16:29:16.8815980Z   - Daily Limit: 50
2025-10-14T16:29:16.8816306Z   - Per-Domain Limit: 5
2025-10-14T16:29:16.8816527Z 
2025-10-14T16:29:16.8816767Z 📤 LIVE MODE: Executing actual campaign
2025-10-14T16:29:16.8817060Z 
2025-10-14T16:29:16.8817963Z Executing: python utils/integrated_runner.py --contacts contacts --scheduled scheduled-campaigns --tracking tracking --templates campaign-templates --alerts alerts@modelphysmat.com
2025-10-14T16:29:16.8818999Z 
2025-10-14T16:29:33.6826303Z ================================================================================
2025-10-14T16:29:33.6826869Z INTEGRATED EMAIL CAMPAIGN SYSTEM
2025-10-14T16:29:33.6827351Z ================================================================================
2025-10-14T16:29:33.6827924Z Start time: 2025-10-14 16:29:16.914931
2025-10-14T16:29:33.6828721Z Mode: LIVE
2025-10-14T16:29:33.6828945Z Contacts dir: contacts
2025-10-14T16:29:33.6829218Z Scheduled dir: scheduled-campaigns
2025-10-14T16:29:33.6829513Z Tracking dir: tracking
2025-10-14T16:29:33.6829763Z Templates dir: campaign-templates
2025-10-14T16:29:33.6830084Z Alerts email: alerts@modelphysmat.com
2025-10-14T16:29:33.6830558Z Tracking directory ready: tracking
2025-10-14T16:29:33.6830865Z 
2025-10-14T16:29:33.6831309Z 🔍 Validating system setup...
2025-10-14T16:29:33.6831685Z ✅ Found contacts directory: contacts
2025-10-14T16:29:33.6832075Z ✅ Found scheduled directory: scheduled-campaigns
2025-10-14T16:29:33.6832460Z ✅ Found tracking directory: tracking
2025-10-14T16:29:33.6832834Z ✅ Found templates directory: campaign-templates
2025-10-14T16:29:33.6833065Z 
2025-10-14T16:29:33.6833500Z 📂 Checking utils directory: /home/runner/work/email-campaign-manager/email-campaign-manager/utils
2025-10-14T16:29:33.6834316Z ✅ Found data_loader.py
2025-10-14T16:29:33.6834612Z ✅ Found docx_parser.py
2025-10-14T16:29:33.6834899Z ✅ Found generate_summary.py
2025-10-14T16:29:33.6835209Z ✅ Found 4 contact files in contacts
2025-10-14T16:29:33.6835586Z ✅ Found 2 campaign files in scheduled-campaigns
2025-10-14T16:29:33.6835991Z ✅ requests library available
2025-10-14T16:29:33.6836297Z ✅ pandas library available
2025-10-14T16:29:33.6836468Z 
2025-10-14T16:29:33.6836584Z ================================================================================
2025-10-14T16:29:33.6836902Z STEP 1: CONTACT LOADING
2025-10-14T16:29:33.6837160Z ================================================================================
2025-10-14T16:29:33.6837545Z 🔍 Loading contacts from directory: contacts
2025-10-14T16:29:33.6838474Z ❌ Failed to import data_loader: cannot import name 'load_contacts' from 'data_loader' (/home/runner/work/email-campaign-manager/email-campaign-manager/utils/data_loader.py)
2025-10-14T16:29:33.6839269Z WARNING: No contacts could be loaded
2025-10-14T16:29:33.6839657Z Continuing with campaign processing (may fail without contacts)
2025-10-14T16:29:33.6839957Z 
2025-10-14T16:29:33.6840071Z ================================================================================
2025-10-14T16:29:33.6840388Z STEP 2: CAMPAIGN PROCESSING
2025-10-14T16:29:33.6840664Z ================================================================================
2025-10-14T16:29:33.6840938Z 
2025-10-14T16:29:33.6841035Z ============================================================
2025-10-14T16:29:33.6841297Z STEP: Campaign Processing
2025-10-14T16:29:33.6841517Z ============================================================
2025-10-14T16:29:33.6842458Z Command: python /home/runner/work/email-campaign-manager/email-campaign-manager/utils/docx_parser.py --contacts contacts --scheduled scheduled-campaigns --tracking tracking --templates campaign-templates --alerts alerts@modelphysmat.com
2025-10-14T16:29:33.6843598Z Exit code: 0
2025-10-14T16:29:33.6843724Z 
2025-10-14T16:29:33.6843795Z STDOUT:
2025-10-14T16:29:33.6844232Z ✅ UnsubscribeManager initialized
2025-10-14T16:29:33.6844553Z    Base URL: https://sednabcn.github.io/unsubscribe
2025-10-14T16:29:33.6844850Z    Unsubscribed count: 1
2025-10-14T16:29:33.6845330Z Unsubscribe link: https://sednabcn.github.io/unsubscribe?email=test%40example.com&campaign=campaign1&token=58a13014
2025-10-14T16:29:33.6845831Z Is unsubscribed: False
2025-10-14T16:29:33.6846168Z 📛 Added test@example.com to unsubscribe list (campaign: all)
2025-10-14T16:29:33.6846644Z Unsubscribe stats: {'total_unsubscribed': 2, 'global_unsubscribes': 2, 'campaign_specific': 0}
2025-10-14T16:29:33.6846969Z 
2025-10-14T16:29:33.6847048Z Enhanced HTML:
2025-10-14T16:29:33.6847298Z <html><body><h1>Test</h1><p>Content here</p></body></html>
2025-10-14T16:29:33.6847685Z <hr style="margin-top: 30px; border: none; border-top: 1px solid #ccc;">
2025-10-14T16:29:33.6848134Z <div style="font-size: 11px; color: #666; margin-top: 15px; text-align: center;">
2025-10-14T16:29:33.6848527Z     <p><strong>Professional Outreach</strong></p>
2025-10-14T16:29:33.6849054Z     <p>You received this email as part of professional networking outreach.</p>
2025-10-14T16:29:33.6849402Z     <p>
2025-10-14T16:29:33.6849633Z         If you prefer not to receive future emails, you can 
2025-10-14T16:29:33.6850362Z         <a href="https://sednabcn.github.io/unsubscribe?email=test%40example.com&campaign=campaign1&token=58a13014" style="color: #0066cc; text-decoration: underline;">unsubscribe here</a>.
2025-10-14T16:29:33.6851029Z     </p>
2025-10-14T16:29:33.6851263Z     <p style="font-size: 10px; color: #999; margin-top: 10px;">
2025-10-14T16:29:33.6851780Z         This is professional outreach. We respect your preferences and will honor all opt-out requests immediately.
2025-10-14T16:29:33.6852223Z     </p>
2025-10-14T16:29:33.6852387Z </div>
2025-10-14T16:29:33.6852480Z 
2025-10-14T16:29:33.6852581Z GitHub Actions email sender available
2025-10-14T16:29:33.6852852Z Using professional data_loader module
2025-10-14T16:29:33.6853125Z Domain-Aware Campaign System Script started
2025-10-14T16:29:33.6853406Z Remote environment: True
2025-10-14T16:29:33.6853711Z Available modules: docx=True, email_sender=True, data_loader=True
2025-10-14T16:29:33.6854203Z Parsing arguments...
2025-10-14T16:29:33.6854338Z 
2025-10-14T16:29:33.6854431Z Arguments parsed successfully:
2025-10-14T16:29:33.6854666Z   --contacts: contacts
2025-10-14T16:29:33.6854888Z   --scheduled: campaign-templates
2025-10-14T16:29:33.6855127Z   --tracking: tracking
2025-10-14T16:29:33.6855340Z   --alerts: alerts@modelphysmat.com
2025-10-14T16:29:33.6855582Z   --feedback: None
2025-10-14T16:29:33.6855778Z   --template-file: None
2025-10-14T16:29:33.6855983Z   --domain: None
2025-10-14T16:29:33.6856169Z   --dry-run: False
2025-10-14T16:29:33.6856359Z   --queue-emails: False
2025-10-14T16:29:33.6856560Z   --compliance: False
2025-10-14T16:29:33.6856758Z   --debug: False
2025-10-14T16:29:33.6856880Z 
2025-10-14T16:29:33.6856977Z Calling domain-aware campaign_main...
2025-10-14T16:29:33.6857242Z Starting domain-aware campaign system
2025-10-14T16:29:33.6857495Z GitHub Actions detected: True
2025-10-14T16:29:33.6857720Z Queue mode: False
2025-10-14T16:29:33.6857909Z Dry run mode: False
2025-10-14T16:29:33.6858107Z Compliance mode: False
2025-10-14T16:29:33.6858306Z Contacts: contacts
2025-10-14T16:29:33.6858530Z Templates (domain-based): campaign-templates
2025-10-14T16:29:33.6858790Z Tracking: tracking
2025-10-14T16:29:33.6859000Z Alerts: alerts@modelphysmat.com
2025-10-14T16:29:33.6859245Z Loading contacts for validation...
2025-10-14T16:29:33.6859415Z 
2025-10-14T16:29:33.6859419Z 
2025-10-14T16:29:33.6859504Z === VALIDATION SUMMARY ===
2025-10-14T16:29:33.6859718Z Total contacts: 9
2025-10-14T16:29:33.6859908Z Valid contacts: 9
2025-10-14T16:29:33.6860092Z Valid emails: 9
2025-10-14T16:29:33.6860277Z Missing emails: 0
2025-10-14T16:29:33.6860481Z Missing names: 0
2025-10-14T16:29:33.6860786Z Unique domains: 6
2025-10-14T16:29:33.6861052Z ✅ Loaded 9 contacts globally for validation
2025-10-14T16:29:33.6861458Z ⚠️  Global compliance filtering disabled - applied per-campaign
2025-10-14T16:29:33.6861706Z 
2025-10-14T16:29:33.6861832Z ✅ UnsubscribeManager initialized
2025-10-14T16:29:33.6862121Z    Base URL: https://sednabcn.github.io/unsubscribe
2025-10-14T16:29:33.6862414Z    Unsubscribed count: 2
2025-10-14T16:29:33.6862916Z ✅ Unsubscribe system initialized: {'total_unsubscribed': 2, 'global_unsubscribes': 2, 'campaign_specific': 0}
2025-10-14T16:29:33.6863293Z 
2025-10-14T16:29:33.6863437Z Using GitHubActionsEmailSender - SMTP timeouts bypassed
2025-10-14T16:29:33.6863855Z EmailSender initialized - dry_run: False, alerts: alerts@modelphysmat.com
2025-10-14T16:29:33.6864491Z GitHub Actions mode - emails will be processed by workflow action
2025-10-14T16:29:33.6864881Z Found 1 campaign(s) in healthcare/ (including subdirectories)
2025-10-14T16:29:33.6865263Z Found 3 campaign(s) in education/ (including subdirectories)
2025-10-14T16:29:33.6865603Z   Subdirectories in education/: adult_education
2025-10-14T16:29:33.6866067Z Found 1 campaign(s) in finance/ (including subdirectories)
2025-10-14T16:29:33.6866285Z 
2025-10-14T16:29:33.6866386Z ======================================================================
2025-10-14T16:29:33.6866658Z SCANNING AND VALIDATING CAMPAIGNS
2025-10-14T16:29:33.6866899Z ======================================================================
2025-10-14T16:29:33.6867082Z 
2025-10-14T16:29:33.6867157Z Domain: HEALTHCARE
2025-10-14T16:29:33.6867405Z   🔍 Validating: outreach.docx
2025-10-14T16:29:33.6867663Z   📊 File size: 36.02 KB
2025-10-14T16:29:33.6867900Z   ✅ DOCX structure valid
2025-10-14T16:29:33.6868141Z   ✅ Extracted 384 characters
2025-10-14T16:29:33.6868439Z   📅 Validating schedule: mode=immediate, date=None
2025-10-14T16:29:33.6868755Z   ✅ Queued (IMMEDIATE): outreach
2025-10-14T16:29:33.6868907Z 
2025-10-14T16:29:33.6868987Z Domain: EDUCATION
2025-10-14T16:29:33.6869268Z   🔍 Validating: adult_education_letter_general.docx
2025-10-14T16:29:33.6869574Z   📊 File size: 6.86 KB
2025-10-14T16:29:33.6869817Z   ✅ DOCX structure valid
2025-10-14T16:29:33.6870056Z   ✅ Extracted 2680 characters
2025-10-14T16:29:33.6870355Z   📅 Validating schedule: mode=immediate, date=None
2025-10-14T16:29:33.6870712Z   ✅ Queued (IMMEDIATE): adult_education_letter_general
2025-10-14T16:29:33.6871052Z   🔍 Validating: adult_education_letter.docx
2025-10-14T16:29:33.6871334Z   📊 File size: 6.87 KB
2025-10-14T16:29:33.6871563Z   ✅ DOCX structure valid
2025-10-14T16:29:33.6871806Z   ✅ Extracted 2684 characters
2025-10-14T16:29:33.6872101Z   📅 Validating schedule: mode=immediate, date=None
2025-10-14T16:29:33.6872440Z   ✅ Queued (IMMEDIATE): adult_education_letter
2025-10-14T16:29:33.6872777Z   📅 Validating schedule: mode=immediate, date=None
2025-10-14T16:29:33.6873101Z   ✅ Queued (IMMEDIATE): welcome_campaign
2025-10-14T16:29:33.6873275Z 
2025-10-14T16:29:33.6873354Z Domain: FINANCE
2025-10-14T16:29:33.6873585Z   🔍 Validating: outreach.docx
2025-10-14T16:29:33.6873841Z   📊 File size: 36.02 KB
2025-10-14T16:29:33.6874277Z   ✅ DOCX structure valid
2025-10-14T16:29:33.6874523Z   ✅ Extracted 384 characters
2025-10-14T16:29:33.6874825Z   📅 Validating schedule: mode=immediate, date=None
2025-10-14T16:29:33.6875135Z   ✅ Queued (IMMEDIATE): outreach
2025-10-14T16:29:33.6875293Z 
2025-10-14T16:29:33.6875389Z ======================================================================
2025-10-14T16:29:33.6875651Z CAMPAIGN QUEUE SUMMARY
2025-10-14T16:29:33.6875873Z ======================================================================
2025-10-14T16:29:33.6876134Z Immediate:     5 campaigns
2025-10-14T16:29:33.6876352Z Schedule Now:  0 campaigns
2025-10-14T16:29:33.6876567Z Scheduled:     0 campaigns
2025-10-14T16:29:33.6876772Z Total Queued:  5 campaigns
2025-10-14T16:29:33.6876982Z Skipped:       0 campaigns
2025-10-14T16:29:33.6877201Z ======================================================================
2025-10-14T16:29:33.6877512Z 
2025-10-14T16:29:33.6877518Z 
2025-10-14T16:29:33.6877608Z ======================================================================
2025-10-14T16:29:33.6877891Z PROCESSING IMMEDIATE CAMPAIGNS (5)
2025-10-14T16:29:33.6878138Z ======================================================================
2025-10-14T16:29:33.6878318Z 
2025-10-14T16:29:33.6878322Z 
2025-10-14T16:29:33.6878417Z --- Campaign: healthcare/outreach ---
2025-10-14T16:29:33.6878691Z   Campaign ID: general_outreach_20251014_162917
2025-10-14T16:29:33.6878972Z   Tracking: tracking/general/outreach
2025-10-14T16:29:33.6879239Z   Archive: contact_details_used/general/outreach
2025-10-14T16:29:33.6879561Z   📂 Loading contacts from: contacts
2025-10-14T16:29:33.6879720Z 
2025-10-14T16:29:33.6879809Z === VALIDATION SUMMARY ===
2025-10-14T16:29:33.6880015Z Total contacts: 9
2025-10-14T16:29:33.6880200Z Valid contacts: 9
2025-10-14T16:29:33.6880385Z Valid emails: 9
2025-10-14T16:29:33.6880558Z Missing emails: 0
2025-10-14T16:29:33.6880748Z Missing names: 0
2025-10-14T16:29:33.6880931Z Unique domains: 6
2025-10-14T16:29:33.6881296Z     ✅ Loaded: 9 valid contacts
2025-10-14T16:29:33.6881564Z   📍 Expected subdirectory: contacts
2025-10-14T16:29:33.6881850Z   📧 Campaign-specific contacts: 9
2025-10-14T16:29:33.6882188Z   📋 Sample contact: alerts@modelphysmat.com - Peter Pan
2025-10-14T16:29:33.6882758Z   📋 Contact fields: ['name', 'rank/title', 'position', 'email', 'phone', 'organization', 'sector', 'address', 'source']
2025-10-14T16:29:33.6883265Z   📄 Processing 9 campaign-specific contacts...
2025-10-14T16:29:33.6883570Z   ✅ Ready to send: 9 contacts
2025-10-14T16:29:33.6883814Z   📁 Source: contacts
2025-10-14T16:29:33.6884279Z Starting campaign 'healthcare/outreach' to 9 recipients
2025-10-14T16:29:33.6884687Z [QUEUED] alerts@modelphysmat.com: Welcome Peter Pan to Our Platform
2025-10-14T16:29:33.6885077Z ✅ Sent 1/9: alerts@modelphysmat.com
2025-10-14T16:29:33.6885444Z [QUEUED] alerts@modelphysmat.com: Welcome Shabnam Beheshti to Our Platform
2025-10-14T16:29:33.6885845Z ✅ Sent 2/9: alerts@modelphysmat.com
2025-10-14T16:29:33.6886206Z [QUEUED] alerts@modelphysmat.com: Welcome Daniel Reidenbach to Our Platform
2025-10-14T16:29:33.6886602Z ✅ Sent 3/9: alerts@modelphysmat.com
2025-10-14T16:29:33.6886938Z [QUEUED] alerts@modelphysmat.com: Welcome Rachel Hilliam to Our Platform
2025-10-14T16:29:33.6887325Z ✅ Sent 4/9: alerts@modelphysmat.com
2025-10-14T16:29:33.6887635Z [QUEUED] john.doe@example.com: Welcome John Doe to Our Platform
2025-10-14T16:29:33.6887990Z ✅ Sent 5/9: john.doe@example.com
2025-10-14T16:29:33.6888297Z [QUEUED] jane.smith@test.org: Welcome Jane Smith to Our Platform
2025-10-14T16:29:33.6888650Z ✅ Sent 6/9: jane.smith@test.org
2025-10-14T16:29:33.6888957Z [QUEUED] bob.johnson@sample.net: Welcome Bob Johnson to Our Platform
2025-10-14T16:29:33.6889329Z ✅ Sent 7/9: bob.johnson@sample.net
2025-10-14T16:29:33.6889648Z [QUEUED] alice.brown@demo.edu: Welcome Alice Brown to Our Platform
2025-10-14T16:29:33.6890018Z ✅ Sent 8/9: alice.brown@demo.edu
2025-10-14T16:29:33.6890349Z [QUEUED] charlie.wilson@tech.co: Welcome Charlie Wilson to Our Platform
2025-10-14T16:29:33.6890734Z ✅ Sent 9/9: charlie.wilson@tech.co
2025-10-14T16:29:33.6890893Z 
2025-10-14T16:29:33.6890995Z Campaign 'healthcare/outreach' completed:
2025-10-14T16:29:33.6891264Z   ✅ Sent: 9
2025-10-14T16:29:33.6891457Z   ❌ Failed: 0
2025-10-14T16:29:33.6891676Z   ⏱️ Duration: 0:00:16.001023
2025-10-14T16:29:33.6892148Z Warning: Could not save campaign results: [Errno 2] No such file or directory: 'tracking/healthcare/outreach_20251014_162933.json'
2025-10-14T16:29:33.6892656Z Saved 9 emails for GitHub Actions processing
2025-10-14T16:29:33.6892939Z Summary: github_actions_email_summary.json
2025-10-14T16:29:33.6893252Z Batch directory: github_actions_emails/healthcare/outreach
2025-10-14T16:29:33.6893588Z   ✅ Campaign complete:
2025-10-14T16:29:33.6893784Z      - Sent: 9
2025-10-14T16:29:33.6894107Z      - Queued: 0
2025-10-14T16:29:33.6894313Z      - Failed: 0
2025-10-14T16:29:33.6894644Z      - Source verified: contacts
2025-10-14T16:29:33.6894937Z   📦 Archiving processed contacts...
2025-10-14T16:29:33.6895226Z   ✅ Archived directory: contacts
2025-10-14T16:29:33.6895606Z      → contact_details_used/general/outreach/contacts_used_20251014_162933
2025-10-14T16:29:33.6895998Z   📁 Created empty replacement: contacts
2025-10-14T16:29:33.6896369Z   ✅ Contacts archived to contact_details_used/general/outreach
2025-10-14T16:29:33.6896598Z 
2025-10-14T16:29:33.6896745Z --- Campaign: education/adult_education_letter_general ---
2025-10-14T16:29:33.6897123Z   Campaign ID: general_adult_education_letter_general_20251014_162933
2025-10-14T16:29:33.6897501Z   Tracking: tracking/general/adult_education_letter_general
2025-10-14T16:29:33.6897890Z   Archive: contact_details_used/general/adult_education_letter_general
2025-10-14T16:29:33.6898262Z   📂 Loading contacts from: contacts
2025-10-14T16:29:33.6898549Z     ⚠️ No contacts loaded from contacts
2025-10-14T16:29:33.6898874Z   ⚠️ No contacts loaded from contacts - SKIPPING
2025-10-14T16:29:33.6899068Z 
2025-10-14T16:29:33.6899184Z --- Campaign: education/adult_education_letter ---
2025-10-14T16:29:33.6899648Z   Campaign ID: general_adult_education_letter_20251014_162933
2025-10-14T16:29:33.6899987Z   Tracking: tracking/general/adult_education_letter
2025-10-14T16:29:33.6900332Z   Archive: contact_details_used/general/adult_education_letter
2025-10-14T16:29:33.6900687Z   📂 Loading contacts from: contacts
2025-10-14T16:29:33.6900972Z     ⚠️ No contacts loaded from contacts
2025-10-14T16:29:33.6901280Z   ⚠️ No contacts loaded from contacts - SKIPPING
2025-10-14T16:29:33.6901464Z 
2025-10-14T16:29:33.6901576Z --- Campaign: education/welcome_campaign ---
2025-10-14T16:29:33.6901883Z   Campaign ID: general_welcome_campaign_20251014_162933
2025-10-14T16:29:33.6902188Z   Tracking: tracking/general/welcome_campaign
2025-10-14T16:29:33.6902503Z   Archive: contact_details_used/general/welcome_campaign
2025-10-14T16:29:33.6902843Z   📂 Loading contacts from: contacts
2025-10-14T16:29:33.6903131Z     ⚠️ No contacts loaded from contacts
2025-10-14T16:29:33.6903444Z   ⚠️ No contacts loaded from contacts - SKIPPING
2025-10-14T16:29:33.6903636Z 
2025-10-14T16:29:33.6903726Z --- Campaign: finance/outreach ---
2025-10-14T16:29:33.6904152Z   Campaign ID: general_outreach_20251014_162933
2025-10-14T16:29:33.6904436Z   Tracking: tracking/general/outreach
2025-10-14T16:29:33.6904709Z   Archive: contact_details_used/general/outreach
2025-10-14T16:29:33.6905024Z   📂 Loading contacts from: contacts
2025-10-14T16:29:33.6905305Z     ⚠️ No contacts loaded from contacts
2025-10-14T16:29:33.6905611Z   ⚠️ No contacts loaded from contacts - SKIPPING
2025-10-14T16:29:33.6905793Z 
2025-10-14T16:29:33.6905894Z ======================================================================
2025-10-14T16:29:33.6906159Z PROCESSING DOMAIN: HEALTHCARE
2025-10-14T16:29:33.6906398Z ======================================================================
2025-10-14T16:29:33.6906577Z 
2025-10-14T16:29:33.6906696Z --- Processing Campaign: healthcare/outreach ---
2025-10-14T16:29:33.6907007Z   🔍 Validating: outreach.docx
2025-10-14T16:29:33.6907273Z   📊 File size: 36.02 KB
2025-10-14T16:29:33.6907512Z   ✅ DOCX structure valid
2025-10-14T16:29:33.6907753Z   ✅ Extracted 384 characters
2025-10-14T16:29:33.6907991Z   No eligible contacts for this campaign
2025-10-14T16:29:33.6908164Z 
2025-10-14T16:29:33.6908261Z ======================================================================
2025-10-14T16:29:33.6908518Z PROCESSING DOMAIN: EDUCATION
2025-10-14T16:29:33.6908746Z ======================================================================
2025-10-14T16:29:33.6908921Z 
2025-10-14T16:29:33.6909151Z --- Processing Campaign: education/adult_education/adult_education_letter_general ---
2025-10-14T16:29:33.6909630Z   🔍 Validating: adult_education_letter_general.docx
2025-10-14T16:29:33.6909934Z   📊 File size: 6.86 KB
2025-10-14T16:29:33.6910162Z   ✅ DOCX structure valid
2025-10-14T16:29:33.6910543Z   ✅ Extracted 2680 characters
2025-10-14T16:29:33.6910785Z   No eligible contacts for this campaign
2025-10-14T16:29:33.6910991Z 
2025-10-14T16:29:33.6911190Z --- Processing Campaign: education/adult_education/adult_education_letter ---
2025-10-14T16:29:33.6911620Z   🔍 Validating: adult_education_letter.docx
2025-10-14T16:29:33.6911903Z   📊 File size: 6.87 KB
2025-10-14T16:29:33.6912135Z   ✅ DOCX structure valid
2025-10-14T16:29:33.6912380Z   ✅ Extracted 2684 characters
2025-10-14T16:29:33.6912614Z   No eligible contacts for this campaign
2025-10-14T16:29:33.6912783Z 
2025-10-14T16:29:33.6912918Z --- Processing Campaign: education/welcome_campaign ---
2025-10-14T16:29:33.6913223Z   No eligible contacts for this campaign
2025-10-14T16:29:33.6913387Z 
2025-10-14T16:29:33.6913488Z ======================================================================
2025-10-14T16:29:33.6913748Z PROCESSING DOMAIN: FINANCE
2025-10-14T16:29:33.6914133Z ======================================================================
2025-10-14T16:29:33.6914332Z 
2025-10-14T16:29:33.6914441Z --- Processing Campaign: finance/outreach ---
2025-10-14T16:29:33.6914900Z   🔍 Validating: outreach.docx
2025-10-14T16:29:33.6915155Z   📊 File size: 36.02 KB
2025-10-14T16:29:33.6915392Z   ✅ DOCX structure valid
2025-10-14T16:29:33.6915635Z   ✅ Extracted 384 characters
2025-10-14T16:29:33.6915871Z   No eligible contacts for this campaign
2025-10-14T16:29:33.6916214Z Campaign summary saved for GitHub Actions: campaign_summary_email.json
2025-10-14T16:29:33.6916604Z Campaign summary saved for GitHub Actions email delivery
2025-10-14T16:29:33.6916819Z 
2025-10-14T16:29:33.6916916Z ======================================================================
2025-10-14T16:29:33.6917162Z FINAL SUMMARY
2025-10-14T16:29:33.6917359Z ======================================================================
2025-10-14T16:29:33.6917612Z Domains processed: 3
2025-10-14T16:29:33.6917820Z Campaigns processed: 1
2025-10-14T16:29:33.6918019Z Emails sent: 9
2025-10-14T16:29:33.6918208Z Emails queued: 0
2025-10-14T16:29:33.6918393Z Failures: 0
2025-10-14T16:29:33.6918580Z Tracking system: DOMAIN-BASED
2025-10-14T16:29:33.6918821Z Template processing: ENABLED
2025-10-14T16:29:33.6918971Z 
2025-10-14T16:29:33.6919060Z Campaign completed successfully
2025-10-14T16:29:33.6919211Z 
2025-10-14T16:29:33.6919392Z ✅ Domain-aware campaign system completed successfully
2025-10-14T16:29:33.8045247Z 
2025-10-14T16:29:33.8045880Z ✅ Campaign Processing completed successfully
2025-10-14T16:29:33.8046225Z 
2025-10-14T16:29:33.8046401Z ================================================================================
2025-10-14T16:29:33.8046844Z STEP 3: SUMMARY GENERATION
2025-10-14T16:29:33.8047222Z ================================================================================
2025-10-14T16:29:33.8047668Z Using log file: campaign_execution.log
2025-10-14T16:29:33.8047936Z 
2025-10-14T16:29:33.8048079Z ============================================================
2025-10-14T16:29:33.8048476Z STEP: Summary Generation
2025-10-14T16:29:33.8048906Z ============================================================
2025-10-14T16:29:33.8050883Z Command: python /home/runner/work/email-campaign-manager/email-campaign-manager/utils/generate_summary.py --log-file campaign_execution.log --mode live --contacts-dir contacts --show-contacts --max-contacts-display 10 --output-summary tracking/campaign_summary.md
2025-10-14T16:29:33.8052793Z Exit code: 0
2025-10-14T16:29:33.8052992Z 
2025-10-14T16:29:33.8053130Z STDOUT:
2025-10-14T16:29:33.8053505Z Processing log file: campaign_execution.log
2025-10-14T16:29:33.8053940Z Mode: live
2025-10-14T16:29:33.8054399Z Show contacts: True
2025-10-14T16:29:33.8054741Z Output file: tracking/campaign_summary.md
2025-10-14T16:29:33.8055151Z Extracting metrics from log file...
2025-10-14T16:29:33.8055550Z Found 1 campaigns, 0 contacts
2025-10-14T16:29:33.8055908Z Loading actual contacts from: contacts
2025-10-14T16:29:33.8056304Z No .url files found in contacts
2025-10-14T16:29:33.8057107Z ⚠️ No actual contacts loaded - will show log-based data only
2025-10-14T16:29:33.8057623Z Building summary report...
2025-10-14T16:29:33.8058101Z ✅ Summary written to tracking/campaign_summary.md
2025-10-14T16:29:33.8058555Z Summary generation completed successfully
2025-10-14T16:29:33.8058840Z 
2025-10-14T16:29:33.8059066Z ✅ Summary Generation completed successfully
2025-10-14T16:29:33.8059563Z Summary generated successfully: tracking/campaign_summary.md
2025-10-14T16:29:33.8059931Z 
2025-10-14T16:29:33.8060044Z SUMMARY PREVIEW:
2025-10-14T16:29:33.8060439Z ------------------------------------------------------------
2025-10-14T16:29:33.8060960Z Processing log file: campaign_execution.log
2025-10-14T16:29:33.8061359Z Mode: live
2025-10-14T16:29:33.8061622Z Show contacts: True
2025-10-14T16:29:33.8061957Z Output file: tracking/campaign_summary.md
2025-10-14T16:29:33.8062401Z Extracting metrics from log file...
2025-10-14T16:29:33.8062788Z Found 1 campaigns, 0 contacts
2025-10-14T16:29:33.8063237Z Loading actual contacts from: contacts
2025-10-14T16:29:33.8063636Z No .url files found in contacts
2025-10-14T16:29:33.8064728Z ⚠️ No actual contacts loaded - will show log-based data only
2025-10-14T16:29:33.8065194Z Building summary report...
2025-10-14T16:29:33.8065669Z ✅ Summary written to tracking/campaign_summary.md
2025-10-14T16:29:33.8066133Z Summary generation completed successfully
2025-10-14T16:29:33.8066412Z 
2025-10-14T16:29:33.8066575Z ------------------------------------------------------------
2025-10-14T16:29:33.8066879Z 
2025-10-14T16:29:33.8067022Z ================================================================================
2025-10-14T16:29:33.8067417Z EXECUTION COMPLETE
2025-10-14T16:29:33.8067743Z ================================================================================
2025-10-14T16:29:33.8068157Z Contacts loaded: 0 (WARNING)
2025-10-14T16:29:33.8068469Z Mode: LIVE
2025-10-14T16:29:33.8068621Z 
2025-10-14T16:29:33.8068763Z Generated files in tracking:
2025-10-14T16:29:33.8069100Z   - .gitkeep (0 bytes)
2025-10-14T16:29:33.8069450Z   - campaign_summary.md (1,129 bytes)
2025-10-14T16:29:33.8069827Z   - rate_limits.json (142 bytes)
2025-10-14T16:29:33.8070191Z   - unsubscribed.json (302 bytes)
2025-10-14T16:29:33.8070448Z 
2025-10-14T16:29:33.8070561Z Log files generated:
2025-10-14T16:29:33.8070885Z   - campaign_execution.log (425 bytes)
2025-10-14T16:29:33.8071146Z 
2025-10-14T16:29:33.8071280Z Final Status: PARTIAL
2025-10-14T16:29:33.8071592Z Completed: 2025-10-14 16:29:33.804339
2025-10-14T16:29:33.8536575Z 
2025-10-14T16:29:33.8536858Z Exit code: 0
2025-10-14T16:29:33.8537403Z ✅ Campaign execution completed successfully
2025-10-14T16:29:33.8566594Z ##[group]Run echo "📊 POST-CAMPAIGN COMPLIANCE REPORT"
2025-10-14T16:29:33.8567031Z [36;1mecho "📊 POST-CAMPAIGN COMPLIANCE REPORT"[0m
2025-10-14T16:29:33.8567348Z [36;1mecho "===================================="[0m
2025-10-14T16:29:33.8567619Z [36;1mecho ""[0m
2025-10-14T16:29:33.8567800Z [36;1m[0m
2025-10-14T16:29:33.8567982Z [36;1m# Show updated stats[0m
2025-10-14T16:29:33.8568221Z [36;1mpython3 << 'PYEOF'[0m
2025-10-14T16:29:33.8568446Z [36;1mimport json[0m
2025-10-14T16:29:33.8568679Z [36;1mfrom pathlib import Path[0m
2025-10-14T16:29:33.8568988Z [36;1mfrom compliance_wrapper import MinimalCompliance[0m
2025-10-14T16:29:33.8569281Z [36;1m[0m
2025-10-14T16:29:33.8569475Z [36;1mcompliance = MinimalCompliance()[0m
2025-10-14T16:29:33.8569752Z [36;1mstats = compliance.get_stats()[0m
2025-10-14T16:29:33.8569993Z [36;1m[0m
2025-10-14T16:29:33.8570191Z [36;1mprint("📊 Final Compliance Status:")[0m
2025-10-14T16:29:33.8570562Z [36;1mprint(f"   Suppressed emails: {stats['suppressed_count']}")[0m
2025-10-14T16:29:33.8570974Z [36;1mprint(f"   Sent today: {stats['sent_today']}/{stats['daily_limit']}")[0m
2025-10-14T16:29:33.8571374Z [36;1mprint(f"   Remaining today: {stats['remaining_today']}")[0m
2025-10-14T16:29:33.8571756Z [36;1mprint(f"   Domains contacted: {stats['domains_contacted']}")[0m
2025-10-14T16:29:33.8572068Z [36;1mprint("")[0m
2025-10-14T16:29:33.8572256Z [36;1m[0m
2025-10-14T16:29:33.8572429Z [36;1m# Check for violations[0m
2025-10-14T16:29:33.8572717Z [36;1mif stats['sent_today'] > stats['daily_limit']:[0m
2025-10-14T16:29:33.8573040Z [36;1m  print("⚠️  WARNING: Daily limit exceeded!")[0m
2025-10-14T16:29:33.8573345Z [36;1m  print(f"   Sent: {stats['sent_today']}")[0m
2025-10-14T16:29:33.8573645Z [36;1m  print(f"   Limit: {stats['daily_limit']}")[0m
2025-10-14T16:29:33.8573901Z [36;1m[0m
2025-10-14T16:29:33.8574294Z [36;1mif stats['remaining_today'] < 5:[0m
2025-10-14T16:29:33.8574682Z [36;1m  print(f"⚠️  WARNING: Near daily limit ({stats['remaining_today']} remaining)")[0m
2025-10-14T16:29:33.8575040Z [36;1m[0m
2025-10-14T16:29:33.8575280Z [36;1m# Show domain breakdown - FIX: Load rate_data properly[0m
2025-10-14T16:29:33.8575631Z [36;1mrate_file = Path('tracking/rate_limits.json')[0m
2025-10-14T16:29:33.8575917Z [36;1mif rate_file.exists():[0m
2025-10-14T16:29:33.8576167Z [36;1m        with open(rate_file) as f:[0m
2025-10-14T16:29:33.8576438Z [36;1m          rate_data = json.load(f)[0m
2025-10-14T16:29:33.8576874Z [36;1m[0m
2025-10-14T16:29:33.8577111Z [36;1m        print("\n📈 Domain Breakdown:")[0m
2025-10-14T16:29:33.8577442Z [36;1m        domain_counts = rate_data.get('domain_counts', {})[0m
2025-10-14T16:29:33.8577745Z [36;1m        if domain_counts:[0m
2025-10-14T16:29:33.8578041Z [36;1m            for domain, count in sorted(domain_counts.items(), [0m
2025-10-14T16:29:33.8578373Z [36;1m                         key=lambda x: x[1], reverse=True):[0m
2025-10-14T16:29:33.8578674Z [36;1m                           print(f"   {domain}: {count}/5")[0m
2025-10-14T16:29:33.8578937Z [36;1m        else:[0m
2025-10-14T16:29:33.8579169Z [36;1m            print("   No domain data available")[0m
2025-10-14T16:29:33.8579434Z [36;1melse:[0m
2025-10-14T16:29:33.8579639Z [36;1m   print("\n📈 Domain Breakdown:")[0m
2025-10-14T16:29:33.8579925Z [36;1m   print("   No rate limit file found yet")[0m
2025-10-14T16:29:33.8580182Z [36;1m[0m
2025-10-14T16:29:33.8580391Z [36;1mprint("\n✅ Compliance report complete")[0m
2025-10-14T16:29:33.8580667Z [36;1mPYEOF[0m
2025-10-14T16:29:33.8580844Z [36;1m[0m
2025-10-14T16:29:33.8581023Z [36;1m# Show rate limit details[0m
2025-10-14T16:29:33.8581254Z [36;1mecho ""[0m
2025-10-14T16:29:33.8581453Z [36;1mecho "📁 Rate Limit Details:"[0m
2025-10-14T16:29:33.8581740Z [36;1mif [ -f tracking/rate_limits.json ]; then[0m
2025-10-14T16:29:33.8582086Z [36;1m   cat tracking/rate_limits.json | python3 -m json.tool[0m
2025-10-14T16:29:33.8582383Z [36;1melse[0m
2025-10-14T16:29:33.8582743Z [36;1m   echo "No rate limit file found"[0m
2025-10-14T16:29:33.8582989Z [36;1mfi[0m
2025-10-14T16:29:33.8583170Z [36;1m[0m
2025-10-14T16:29:33.8583335Z [36;1mecho ""[0m
2025-10-14T16:29:33.8583549Z [36;1mecho "===================================="[0m
2025-10-14T16:29:33.8616028Z shell: /usr/bin/bash -e {0}
2025-10-14T16:29:33.8616264Z env:
2025-10-14T16:29:33.8616458Z   ALERT_EMAIL: alerts@modelphysmat.com
2025-10-14T16:29:33.8616741Z   FEEDBACK_EMAIL: feedback@modelphysmat.com
2025-10-14T16:29:33.8617020Z   PYTHON_VERSION: 3.11
2025-10-14T16:29:33.8617230Z   PRODUCTION_MODE: true
2025-10-14T16:29:33.8617436Z   TRACKING_DIR: tracking
2025-10-14T16:29:33.8617663Z   SCHEDULED_DIR: scheduled-campaigns
2025-10-14T16:29:33.8618037Z   TEMPLATES_DIR: campaign-templates
2025-10-14T16:29:33.8618447Z   CONTACTS_DIR: contacts
2025-10-14T16:29:33.8618778Z   FORCE_IMMEDIATE_SEND: true
2025-10-14T16:29:33.8631656Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:33.8632143Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib/pkgconfig
2025-10-14T16:29:33.8632551Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:33.8632907Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:33.8633264Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.13/x64
2025-10-14T16:29:33.8633625Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.13/x64/lib
2025-10-14T16:29:33.8634108Z   GOOGLE_APPLICATION_CREDENTIALS: /tmp/google_svc.json
2025-10-14T16:29:33.8634403Z ##[endgroup]
2025-10-14T16:29:33.8684673Z 📊 POST-CAMPAIGN COMPLIANCE REPORT
2025-10-14T16:29:33.8685115Z ====================================
2025-10-14T16:29:33.8685360Z 
2025-10-14T16:29:33.8934768Z ✅ Compliance initialized:
2025-10-14T16:29:33.8935238Z    Suppressed: 0
2025-10-14T16:29:33.8935646Z    Sent today: 0/50
2025-10-14T16:29:33.8935922Z    Min delay: 30s between sends
2025-10-14T16:29:33.8936270Z 📊 Final Compliance Status:
2025-10-14T16:29:33.8936570Z    Suppressed emails: 0
2025-10-14T16:29:33.8936833Z    Sent today: 0/50
2025-10-14T16:29:33.8937075Z    Remaining today: 50
2025-10-14T16:29:33.8937322Z    Domains contacted: 0
2025-10-14T16:29:33.8937479Z 
2025-10-14T16:29:33.8937485Z 
2025-10-14T16:29:33.8937621Z 📈 Domain Breakdown:
2025-10-14T16:29:33.8937877Z    No domain data available
2025-10-14T16:29:33.8938045Z 
2025-10-14T16:29:33.8938201Z ✅ Compliance report complete