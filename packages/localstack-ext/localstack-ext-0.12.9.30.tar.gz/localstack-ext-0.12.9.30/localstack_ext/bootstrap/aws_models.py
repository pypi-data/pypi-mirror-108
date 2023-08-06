from localstack.utils.aws import aws_models
vdbSM=super
vdbSA=None
vdbSJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  vdbSM(LambdaLayer,self).__init__(arn)
  self.cwd=vdbSA
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.vdbSJ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,vdbSJ,env=vdbSA):
  vdbSM(RDSDatabase,self).__init__(vdbSJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,vdbSJ,env=vdbSA):
  vdbSM(RDSCluster,self).__init__(vdbSJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,vdbSJ,env=vdbSA):
  vdbSM(AppSyncAPI,self).__init__(vdbSJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,vdbSJ,env=vdbSA):
  vdbSM(AmplifyApp,self).__init__(vdbSJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,vdbSJ,env=vdbSA):
  vdbSM(ElastiCacheCluster,self).__init__(vdbSJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,vdbSJ,env=vdbSA):
  vdbSM(TransferServer,self).__init__(vdbSJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,vdbSJ,env=vdbSA):
  vdbSM(CloudFrontDistribution,self).__init__(vdbSJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,vdbSJ,env=vdbSA):
  vdbSM(CodeCommitRepository,self).__init__(vdbSJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
