class BaseRenderer(object):
    """
    Renderers are used to generate specific configuration blocks.
    """
    block_name = None

    def __init__(self, config, env):
        self.config = config
        self.env = env

    def cleanup(self, output):
        """
        Performs cleanup of output (indentation, new lines)
        """
        output = output.replace('    ', '')\
                       .replace('option', '    option')\
                       .replace('list', '    list')
        # if output is present
        # ensure it always ends with 1 new line
        if output and not output.endswith('\n'):
            output += '\n'
        if output.endswith('\n\n'):
            return output[0:-1]
        return output

    def render(self):
        """
        Renders config block with jinja2 templating engine
        """
        # determine block name
        default_name = str(self.__class__.__name__).replace('Renderer', '').lower()
        block_name = getattr(self, 'block_name') or default_name
        # get jinja2 template
        template_name = '{0}.uci'.format(block_name)
        template = self.env.get_template(template_name)
        # render template and cleanup
        context = self.get_context()
        output = template.render(**context)
        return self.cleanup(output)

    def get_context(self):
        """
        Builds context that is passed to jinja2 templates
        """
        # get list of private methods that start with "_get_"
        methods = [method for method in dir(self) if method.startswith('_get_')]
        context = {}
        # build context
        for method in methods:
            key = method.replace('_get_', '')
            context[key] = getattr(self, method)()
        # determine if all context values are empty
        context['is_empty'] = not any(context.values())
        return context
