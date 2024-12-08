<?php
if (!defined('_PS_VERSION_')) {
    exit;
}

class Yarn_Brandshow extends Module {
public function __construct()
    {
        $this->name = 'yarn_brandshow';
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

        $this->displayName = $this->trans('Yarnstreet carousel of brands', [], 'Modules.Yarnbrandshow.Admin');
        $this->description = $this->trans('Displays a carousel of brands.', [], 'Modules.Yarnbrandshow.Admin');

        $this->confirmUninstall = $this->trans('Are you sure you want to uninstall?', [], 'Modules.Yarnbrandshow.Admin');

        if (!Configuration::get('YARN_BRANDSHOW_NAME')) {
            $this->warning = $this->trans('No name provided', [], 'Modules.Yarnbrandshow.Admin');
        }
    }

public function install()
{
    if (Shop::isFeatureActive()) {
        Shop::setContext(Shop::CONTEXT_ALL);
    }

   return (
        parent::install()
	&& $this->registerHook('home')
        && Configuration::updateValue('YARN_BRANDSHOW_NAME', 'yarn_brandshow')
    );
}

public function uninstall()
{
    return (
        parent::uninstall() 
        && Configuration::deleteByName('YARN_BRANDSHOW_NAME')
    );
}

public function hookDisplayHome($params)
{
  $this->context->smarty->assign(
      array(
          'yarn_brandshow_name' => Configuration::get('YARN_BRANDSHOW_NAME'),
          'yarn_brandshow_link' => $this->context->link->getModuleLink('yarn_brandshow', 'display')
      )
  );
  return $this->display(__FILE__, 'yarn_brandshow.tpl');
}

public function hookDisplayHeader()
{
  $this->context->controller->addCSS($this->_path.'css/yarn_brandshow.css', 'all');
}


}
