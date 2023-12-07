# Oracle for testing

Prerequisite: instrumented target code and runtests.sh in a repo.

1. Create the assignment on Github Classroom, and

2. Select "Add Autograding Tests"
   ```
   Name:  Run Unit Tests
   Setup Command: sudo -H git submodule add https://github.com/someplace/xxxx oracle
   Run Command: oracle/runtests.sh
   Timeout: 5
   ```

3. Test it.
