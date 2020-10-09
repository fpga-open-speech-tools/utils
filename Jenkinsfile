pipeline
{
    agent none
    stages
    {
        stage ('Ubuntu 20.04')
        {
            agent {label 'Ubuntu_20.04.1'}
            stages 
            {
                stage('Check Frost Utils Repo') 
                {
                    parallel
                    {
                        stage('Frost Edge')
                        {
                            when {changeset "frost_edge/**/*"}
                            steps 
                            {
                                build job: 'Frost_Edge'
                            }
                        }
                    }
                }
                stage('Cleanup')
                {
                    steps
                    {
                        deleteDir()
                        dir("${workspace}@tmp") {
                            deleteDir()
                        }
                    }
                } 
            }
        }
    }
}