from buildbot.plugins import util, steps
from buildbot.process import buildstep, logobserver
from twisted.internet import defer
from buildbot.steps import trigger

class DynamicTrigger(trigger.Trigger):

    def getSchedulersAndProperties(self):
        return [
            ("m4.large",
             {
                 'virtual_builder_name': 'virtual_testy',
                 'virtual_builder_description': 'I am a virtual builder',
                 'virtual_builder_tags': ['virtual'],
             }, False),
            ("m4.2xlarge", {
                'virtual_builder_name': 'lsqa',
                'virtual_builder_description': 'I am a virtual builder too',
                'virtual_builder_tags': ['virtual2'],
            }, True)
        ]

class GenerateStagesCommand(buildstep.ShellMixin, steps.BuildStep):

    def __init__(self, **kwargs):
        kwargs = self.setupShellMixin(kwargs)
        steps.BuildStep.__init__(self, **kwargs)
        self.observer = logobserver.BufferLogObserver()
        self.addLogObserver('stdio', self.observer)

    def extract_stages(self, stdout):
        stages = []
        for line in stdout.split('\n'):
            stage = str(line.strip())
            if stage:
                stages.append(stage)
        return stages

    def mkCommand(self, stage):
        return steps.ShellCommand(name=stage,
                                  command=["./build.py", "--run", stage],
                                  haltOnFailure=True)

    @defer.inlineCallbacks
    def run(self):
        # run './build.sh --list-stages' to generate the list of stages
        cmd = yield self.makeRemoteShellCommand()
        yield self.runCommand(cmd)

        # if the command passes extract the list of stages
        result = cmd.results()
        if result == util.SUCCESS:
            # create a ShellCommand for each stage and add them to the build
            stages = self.extract_stages(self.observer.getStdout())
            new_steps = [self.mkCommand(stage) for stage in stages]
            self.build.addStepsAfterCurrentStep(new_steps)

        defer.returnValue(result)

