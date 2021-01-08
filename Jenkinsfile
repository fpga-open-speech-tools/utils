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
                            when {
                                anyOf {
                                    changeset "frost_edge/**/*"
                                    changeset "runtime_config/*"
                                }
                            }
                            steps 
                            {
                                build job: 'Frost_Edge'
                            }
                        }
                        stage ('Image Builder - Audio Mini')
                        {
                            when {
                                anyOf {
                                    changeset "image_builder/frost_usd_card_blueprint.xml"
                                    changeset "image_builder/audiomini/*"
                                }
                            }
                            steps
                            {
                                build job: 'audiomini-linux-image'
                            }
                        }
                        stage('Frost Root File System')
                        {
                            when { changeset "rootfs/*"}
                            steps 
                            {
                                build job: 'Frost_RootFS'
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