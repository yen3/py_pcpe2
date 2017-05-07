node {
    stage "Prepare environment"
    checkout scm
    customWorkspace '/home/jenkins'
    def environment  = docker.build 'pcpe2_ubuntu'
			environment.inside {
					stage "Run ci script"
							sh "./run_ci.sh"
			}
}
