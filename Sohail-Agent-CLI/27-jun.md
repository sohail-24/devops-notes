(venv) sohal@Mohammeds-MacBook-Pro Sohail-Agent-CLI % python -m pytest
========================================================= test session starts =========================================================
platform darwin -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/sohal/Downloads/testing-project/Sohail-Agent-CLI
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.14.0, asyncio-1.4.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 146 items                                                                                                                   

tests/agents/test_blueprint_agent.py ....                                                                                       [  2%]
tests/agents/test_planning_agent.py ...........                                                                                 [ 10%]
tests/agents/test_planning_agent_v2.py .....                                                                                    [ 13%]
tests/agents/test_specification_agent.py ....                                                                                   [ 16%]
tests/agents/test_stack_agent.py ....                                                                                           [ 19%]
tests/ai/test_context.py ...                                                                                                    [ 21%]
tests/ai/test_memory.py ..                                                                                                      [ 22%]
tests/ai/test_orchestrator.py ....                                                                                              [ 25%]
tests/ai/test_prompts.py ...                                                                                                    [ 27%]
tests/ai/test_provider.py ....                                                                                                  [ 30%]
tests/ai/test_response_parser.py .                                                                                              [ 30%]
tests/ai/test_router.py ..                                                                                                      [ 32%]
tests/ai/test_validator.py ............                                                                                         [ 40%]
tests/blueprint/test_blueprint_loader_writer.py .....                                                                           [ 43%]
tests/blueprint/test_blueprint_models.py ..                                                                                     [ 45%]
tests/generators/test_blueprint_generator.py .                                                                                  [ 45%]
tests/generators/test_planning_generator.py .......                                                                             [ 50%]
tests/generators/test_specification_generator.py .                                                                              [ 51%]
tests/generators/test_stack_generator.py ....                                                                                   [ 54%]
tests/planning/decision_engine/test_decision_engine_engine.py ..                                                                [ 55%]
tests/planning/decision_engine/test_decision_engine_models.py ..                                                                [ 56%]
tests/planning/decision_engine/test_decision_engine_renderer.py ....                                                            [ 59%]
tests/planning/decision_engine/test_decision_engine_validator.py .....                                                          [ 63%]
tests/planning/test_models.py .....                                                                                             [ 66%]
tests/planning/test_questions.py .......                                                                                        [ 71%]
tests/providers/test_mock_provider.py ..                                                                                        [ 72%]
tests/providers/test_ollama_provider.py ....                                                                                    [ 75%]
tests/specification/test_loader_writer.py ....                                                                                  [ 78%]
tests/specification/test_specification_models.py ..                                                                             [ 79%]
tests/stack/test_loader.py ...                                                                                                  [ 81%]
tests/stack/test_selector.py ..                                                                                                 [ 82%]
tests/test_cli_blueprint.py ....                                                                                                [ 85%]
tests/test_cli_plan.py .......                                                                                                  [ 90%]
tests/test_cli_plan_v2.py .....                                                                                                 [ 93%]
tests/test_cli_specification.py ....                                                                                            [ 96%]
tests/test_cli_stack.py .....                                                                                                   [100%]

========================================================= 146 passed in 0.33s =========================================================
(venv) sohal@Mohammeds-MacBook-Pro Sohail-Agent-CLI % sohail-agent --help
usage: sohail-agent [-h] [--version] [--verbose] [--dry-run] [--overwrite] [--ollama]
                    {inspect,dockerize,k8s,cicd,docs,interview,plan,plan-v2,bootstrap,stack,specification,blueprint,all} ...

Sohail-Agent-CLI: A local AI engineering assistant

positional arguments:
  {inspect,dockerize,k8s,cicd,docs,interview,plan,plan-v2,bootstrap,stack,specification,blueprint,all}
                        Available commands
    inspect             Inspect repository structure and stack
    dockerize           Generate Docker configuration
    k8s                 Generate Kubernetes manifests
    cicd                Generate CI/CD workflows
    docs                Generate project documentation
    interview           Generate interview notes
    plan                Create a persistent project planning package
    plan-v2             Create a planning package with the Engineering Decision Engine
    bootstrap           Generate a professional project scaffold from a planning package
    stack               Generate technology stack skeletons from a planning package
    specification       Generate structured specification files from a planning package
    blueprint           Generate implementation blueprint files from planning and specification packages
    all                 Run all agents on the project

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --verbose, -v         Enable verbose output
  --dry-run             Show what would be done without making changes
  --overwrite           Overwrite existing files
  --ollama              Use Ollama for AI-enhanced generation (docs, interview)

Examples:
  sohail-agent inspect ./my-project
  sohail-agent dockerize ./my-project
  sohail-agent k8s ./my-project
  sohail-agent cicd ./my-project
  sohail-agent docs ./my-project
  sohail-agent interview ./my-project
  sohail-agent plan "Build an ecommerce platform"
  sohail-agent plan-v2
  sohail-agent stack --plan-dir ./project-plan --output ./my-project
  sohail-agent specification --plan-dir ./project-plan --output ./specifications
  sohail-agent blueprint --plan-dir ./project-plan --spec-dir ./specifications --output ./blueprints
  sohail-agent all ./my-project
        
(venv) sohal@Mohammeds-MacBook-Pro Sohail-Agent-CLI % cd ..
(venv) sohal@Mohammeds-MacBook-Pro testing-project % mkdir deom-1
(venv) sohal@Mohammeds-MacBook-Pro testing-project % cd demo-1
cd: no such file or directory: demo-1
(venv) sohal@Mohammeds-MacBook-Pro testing-project % ls
ai-terminal-dashboard		demo				PLANNING_AGENT_DESIGN.md	sohail-test
bootstrap-demo			deom-1				Sohail-Agent-CLI		strands-temporal-agents
(venv) sohal@Mohammeds-MacBook-Pro testing-project % rm-rf deom-1 
zsh: command not found: rm-rf
(venv) sohal@Mohammeds-MacBook-Pro testing-project % mkdir test-demo
(venv) sohal@Mohammeds-MacBook-Pro testing-project % cd test-demo 
(venv) sohal@Mohammeds-MacBook-Pro test-demo % ls
(venv) sohal@Mohammeds-MacBook-Pro test-demo % sohail-agent plan-v2

## Project
Project identity and product intent.
Project name: sohail-shop
Project goal: admin and user
Target users (comma-separated): 
An answer is required.
Target users (comma-separated): ⚠ Planning cancelled; no files changed
(venv) sohal@Mohammeds-MacBook-Pro test-demo % ls                                
(venv) sohal@Mohammeds-MacBook-Pro test-demo % sohail-agent plan "Build Todo App"
Q-001 — Project name (default: Todo App): ⚠ Planning cancelled; no files changed
(venv) sohal@Mohammeds-MacBook-Pro test-demo % 
