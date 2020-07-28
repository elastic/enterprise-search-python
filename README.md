# Workplace Search Python Generator

## TODOs

- [ ] APIs should be better at detecting whether they are going to be a Response
      subclass or just a dict. Should look at whether the component is used in any API.
- [ ] Need to write the code that guarantees APIs aren't reordered whenever things
      are regenerated and written to an already existing file.
- [x] Need to figure out the param collapsing. Want to avoid a func signature blender like
      is used for ES client. Maybe `params = make_params(params, **kwargs)` works?
- [x] Aliased params like `page_current` -> `page[current]` need to be put back into their wire format.
- [x] Generate App Search API from PHP library YAML
- [ ] Figure out how multi-service authentication should work
      (Current solution uses `<Client>.http_auth = ...` and figures out from
      there if it's token or basic)
