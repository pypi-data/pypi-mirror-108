from localstack.utils.aws import aws_models
zalhp=super
zalhH=None
zalhv=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  zalhp(LambdaLayer,self).__init__(arn)
  self.cwd=zalhH
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.zalhv.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,zalhv,env=zalhH):
  zalhp(RDSDatabase,self).__init__(zalhv,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,zalhv,env=zalhH):
  zalhp(RDSCluster,self).__init__(zalhv,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,zalhv,env=zalhH):
  zalhp(AppSyncAPI,self).__init__(zalhv,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,zalhv,env=zalhH):
  zalhp(AmplifyApp,self).__init__(zalhv,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,zalhv,env=zalhH):
  zalhp(ElastiCacheCluster,self).__init__(zalhv,env=env)
class TransferServer(BaseComponent):
 def __init__(self,zalhv,env=zalhH):
  zalhp(TransferServer,self).__init__(zalhv,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,zalhv,env=zalhH):
  zalhp(CloudFrontDistribution,self).__init__(zalhv,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,zalhv,env=zalhH):
  zalhp(CodeCommitRepository,self).__init__(zalhv,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
