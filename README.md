# Sublimated symfony

Sublime Text 3 (not realy support ST2) package for better Symfony 2 usage.

## Instalation

### Manual installation

```sh
git clone git@github.com:sergeylunev/sublimated-symfony.git \
    ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/sublimated-symfony
```

## Usage

### Switch betwen action and view

`ctrl+alt+p` — if pressed in Action opens template file (or create file and open it).
If pressed in template file — open Controller on Action file related to this template

### Switch betwen entity and repository

`ctrl+alt+g` — If pressed in Entity it send you to Repository class witch is
presented in `@ORM\Entity(repositoryClass="Acme\DemoBundle\Entity\Repository\DemoRepository")`.
If pressed in Repository it send you to entity class file with the same name as
Repository `DemoRepository` → `Demo`

### Importing `use` statements

`ctrl+alt+u` — automaticaly add `use` statement when cursor placed on some object 
defenition (`new FooBar()`)

### Importing `namespace` related to file

`ctrl+alt+n` — automaticaly add `namespace` statement related to file (please look
for [PSR-0][1] for better understanding)

TODO:
- add some screencasts to illustrate how it works
- working with symfony commands
- jump from inline in twig template to another template or to action/controller
- jump to twig file if we have named in annotation
- add commands execution from ST
- working with routes and other stuff
- try add GoTo by route, actions, entity, repository and other
- workign with generators from editor
- go to template file from twig render or include

Complete:
- insert `namespace` related to the file
- jump between entity and repository classes

[1]: https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-0.md
