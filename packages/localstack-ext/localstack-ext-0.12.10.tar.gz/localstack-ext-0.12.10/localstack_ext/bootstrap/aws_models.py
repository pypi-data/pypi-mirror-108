from localstack.utils.aws import aws_models
hLRBX=super
hLRBc=None
hLRBU=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  hLRBX(LambdaLayer,self).__init__(arn)
  self.cwd=hLRBc
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.hLRBU.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,hLRBU,env=hLRBc):
  hLRBX(RDSDatabase,self).__init__(hLRBU,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,hLRBU,env=hLRBc):
  hLRBX(RDSCluster,self).__init__(hLRBU,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,hLRBU,env=hLRBc):
  hLRBX(AppSyncAPI,self).__init__(hLRBU,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,hLRBU,env=hLRBc):
  hLRBX(AmplifyApp,self).__init__(hLRBU,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,hLRBU,env=hLRBc):
  hLRBX(ElastiCacheCluster,self).__init__(hLRBU,env=env)
class TransferServer(BaseComponent):
 def __init__(self,hLRBU,env=hLRBc):
  hLRBX(TransferServer,self).__init__(hLRBU,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,hLRBU,env=hLRBc):
  hLRBX(CloudFrontDistribution,self).__init__(hLRBU,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,hLRBU,env=hLRBc):
  hLRBX(CodeCommitRepository,self).__init__(hLRBU,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
