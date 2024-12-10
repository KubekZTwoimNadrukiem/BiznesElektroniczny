<?php
if (!defined('_PS_VERSION_')) {
    exit;
}

class Yarn_Blog extends Module {
public function __construct()
    {
        $this->name = 'yarn_blog';
        $this->tab = 'front_office_features';
        $this->version = '1.0.0';
        $this->author = 'KubekZMoimNadrukiem';
        $this->need_instance = 0;
        $this->ps_versions_compliancy = [
            'min' => '1.7.0.0',
            'max' => '8.99.99',
        ];
        $this->bootstrap = true;

        parent::__construct();

        $this->displayName = $this->trans('Yarnstreet blog posts carousel', [], 'Modules.Yarnblog.Admin');
        $this->description = $this->trans('Displays a carousel of blog posts.', [], 'Modules.Yarnblog.Admin');

        $this->confirmUninstall = $this->trans('Are you sure you want to uninstall?', [], 'Modules.Yarnblog.Admin');

        if (!Configuration::get('YARN_BLOG_NAME')) {
            $this->warning = $this->trans('No name provided', [], 'Modules.Yarnblog.Admin');
        }
    }

public function install()
{
    if (Shop::isFeatureActive()) {
        Shop::setContext(Shop::CONTEXT_ALL);
    }

   return (
        parent::install()
	&& $this->registerHook('wrapperBottom')
        && Configuration::updateValue('YARN_BLOG_NAME', 'yarn_blog')
    );
}

public function uninstall()
{
    return (
        parent::uninstall() 
        && Configuration::deleteByName('YARN_BLOG_NAME')
    );
}

public function hookDisplayWrapperBottom($params)
{
  $this->context->smarty->assign(
      array(
          'yarn_blog_name' => Configuration::get('YARN_BLOG_NAME'),
          'yarn_blog_link' => $this->context->link->getModuleLink('yarn_blog', 'display')
      )
  );
  return $this->display(__FILE__, 'yarn_blog.tpl');
}

public function hookDisplayHeader()
{
  $this->context->controller->addCSS($this->_path.'css/yarn_blog.css', 'all');
}


}
