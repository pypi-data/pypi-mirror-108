from pyshellrunner import ShellRunner, pyshell_with_values

def test_pyshell_with_values_context_manager():
    s = ShellRunner()
    s.verbosity = 2
    s.cwd = "/"
    s.run("ls home")

    with pyshell_with_values(s) as s2:
        s2.cwd = '/usr'
        s2.run("ls include")

    with pyshell_with_values(s, { 'cwd': '/usr' }) as s2:
        s2.run("ls include")

    s.run("ls home")