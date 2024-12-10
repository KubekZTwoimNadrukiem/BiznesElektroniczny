<?php
if (!defined('_PS_VERSION_')) {
    exit;
}

class Yarn_Howto extends Module {
public function __construct()
    {
        $this->name = 'yarn_howto';
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

        $this->displayName = $this->trans('Yarnstreet how to', [], 'Modules.Yarnhowto.Admin');
        $this->description = $this->trans('How to purchase.', [], 'Modules.Yarnhowto.Admin');

        $this->confirmUninstall = $this->trans('Are you sure you want to uninstall?', [], 'Modules.Yarnhowto.Admin');

        if (!Configuration::get('YARN_HOWTO_NAME')) {
            $this->warning = $this->trans('No name provided', [], 'Modules.Yarnhowto.Admin');
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
        && Configuration::updateValue('YARN_HOWTO__NAME', 'yarn_howto')
    );
}

public function uninstall()
{
    return (
        parent::uninstall() 
        && Configuration::deleteByName('YARN_HOWTO_NAME')
    );
}

public function hookDisplayHome($params)
{
  $this->context->smarty->assign(
      array(
          'yarn_howto_name' => Configuration::get('YARN_HOWTO_NAME'),
          'yarn_howto_link' => $this->context->link->getModuleLink('yarn_howto', 'display')
      )
  );
  return $this->display(__FILE__, 'yarn_howto.tpl');
}

public function hookDisplayHeader()
{
  $this->context->controller->addCSS($this->_path.'css/yarn_howto.css', 'all');
}


}
