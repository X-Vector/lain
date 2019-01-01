# lain
Lain - Interactive Decombiler .
![screenshot at 2019-01-01 07-38-17](https://user-images.githubusercontent.com/22657154/50572997-2b5a3400-0d99-11e9-919f-cb96450ea50c.png)

## Main features
``` info functions || i f ```
```assembly
[#] i f
┌ 
│ 0x080482f8  sym._init
│ 0x08048320  sym.imp.__libc_start_main
│ 0x08048330  sym.imp.scanf
│ 0x08048340  sym.imp.printf
│ 0x08048350  sym.imp.strcmp
│ 0x08048360  entry0
│ 0x08048384  fcn.08048384
│ 0x080483b0  sym.__do_global_dtors_aux
│ 0x080483e0  sym.frame_dummy
│ 0x08048414  main
│ 0x080484a0  sym.__libc_csu_init
│ 0x08048510  sym.__libc_csu_fini
│ 0x08048515  sym.__i686.get_pc_thunk.bx
└ 
```
``` info strings || i s ```
```assembly
[#] i s
┌ 
│ 0x08048568   IOLI Crackme Level 0x00\n
│ 0x08048581   Password: 
│ 0x0804858f   250382
│ 0x08048596   Invalid Password!\n
│ 0x080485a9   Password OK --\n
└ 
```
``` decompile <function> || d <function> ```
```python
[#] d main
┌ 
│ def main(argc, argv):
│     printf("IOLI Crackme Level 0x00\n")
│     printf("Password: ")
│     loc_3 = &loc_4 
│     scanf("%s", loc_3)
│     if strcmp(loc_3, "250382") == 0:
│         printf("Password OK --\n")
│     else:
│         printf("Invalid Password!\n")
│     return 0
└ 
```
``` ? <value> ```
```assembly
[#] ? 0x2345
┌ 
│ hex     0x2345
│ octal   021505
│ unit    8.8K
│ segment 0000:0345
│ int32   9029
│ string  "E#"
│ binary  0b0010001101000101
│ fvalue: 9029.0
│ float:  0.000000f
│ double: 0.000000
│ trits   0t110101102
│ 
└ 
```

``` rename <var> || r <var> ```
``` rename globals <new_global_variables_name> || r globals <...> # Default is glob ``` 
``` rename locals <new_local_variables_name> || r local <...>     # Default is loc  ```

### This Project is under development.
### EOF
