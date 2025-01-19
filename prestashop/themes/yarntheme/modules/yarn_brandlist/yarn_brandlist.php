<?php
if (!defined('_PS_VERSION_')) {
    exit;
}

class Yarn_Brandlist extends Module {
public function __construct()
    {
        $this->name = 'yarn_brandlist';
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

        $this->displayName = $this->trans('Yarnstreet list of brands', [], 'Modules.Yarnbrandlist.Admin');
        $this->description = $this->trans('Displays a list of brands.', [], 'Modules.Yarnbrandlist.Admin');

        $this->confirmUninstall = $this->trans('Are you sure you want to uninstall?', [], 'Modules.Yarnbrandlist.Admin');

        if (!Configuration::get('YARN_BRANDLIST_NAME')) {
            $this->warning = $this->trans('No name provided', [], 'Modules.Yarnbrandlist.Admin');
        }
    }

public function install()
{
    if (Shop::isFeatureActive()) {
        Shop::setContext(Shop::CONTEXT_ALL);
    }

   return (
        parent::install()
	&& $this->registerHook('footerBefore')
        && Configuration::updateValue('YARN_BRANDLIST_NAME', 'yarn_brandlist')
    );
}

public function uninstall()
{
    return (
        parent::uninstall() 
        && Configuration::deleteByName('YARN_BRANDLIST_NAME')
    );
}

public function hookDisplayFooterBefore($params)
{
  $this->context->smarty->assign(
      array(
          'yarn_brandlist_name' => Configuration::get('YARN_BRANDLIST_NAME'),
          'yarn_brandlist_link' => $this->context->link->getModuleLink('yarn_brandlist', 'display')
      )
  );
  return $this->display(__FILE__, 'yarn_brandlist.tpl');
}

public function hookDisplayHeader()
{
  $this->context->controller->addCSS($this->_path.'css/yarn_brandlist.css', 'all');
}


}
